import time
import copy
import random
import logging
import threading
import numpy as np

from .utils.npc import NPC
from .utils.scenario import BaseScenario
from .utils.simple_env import SimpleEnv, make_env
from .utils.core import Agent, Goal, Obstacle, World
from .utils.problems import get_problem_instance

from gymnasium.utils import EzPickle


class raw_env(SimpleEnv, EzPickle):
    def __init__(self, problem_type, num_agents=1, render_mode=None):
        
        if problem_type not in {'disaster_response', 'precision_farming'}:
            raise ValueError("Signal8 only supports 'disaster_response' and 'precision_farming' problem types.")
        
        if num_agents > 2:
            raise ValueError("Signal8 currently can only support up to 2 agents.")
        
        scenario = Scenario()
        world = scenario.make_world(problem_type, num_agents)
        
        super().__init__(
            scenario=scenario, 
            world=world, 
            render_mode=render_mode,
            max_cycles=500, 
        )
        
env = make_env(raw_env)

class Scenario(BaseScenario):
    def make_world(self, problem_type, num_agents):
        world = World()
        self._add_logger()
        world.problem_type = problem_type
        
        self.npc = []
        self.scripted_obstacle_threads = []
        self.scripted_obstacle_running = False

        world.agents = [Agent() for _ in range(num_agents)]
        for i, agent in enumerate(world.agents):
            agent.name = f"agent_{i}"
            agent.collide = True

        # Agents has two goals (i.e., actual goal and start position)
        # This is to ensure agent returns safely to start position
        world.goals = [Goal() for _ in range(len(world.agents*2))]
        for i, goal in enumerate(world.goals):
            goal.name = f"goal_{i}"
            goal.collide = False
        
        # Minimum number of obstacles in a problem instance 
        world.obstacles = [Obstacle() for _ in range(4)]
        for i, obstacle in enumerate(world.obstacles):
            obstacle.name = f"obs_{i}"
                
        return world
    
    # Get constraints on entities given the problem instance name
    def _set_problem_instance(self, world, np_random, instance_num):
        instance_name, instance = get_problem_instance(world.problem_type, instance_num, np_random)
        world.problem_instance = instance_name
        world.start_constr = instance['start']
        world.goal_constr = instance['goal']
        world.static_obstacle_constr = instance['static_obs']
        world.dynamic_obstacle_constr = instance['dynamic_obs']
    
    """
    Returns goal constraints that haven't been selected to be used as an obstacle
    for the precision farming case (i.e., crop that wasn't selected as goal becomes an obstacle)
    """
    def _reset_agents_and_goals(self, world, np_random):
        temp_goal_constr = copy.copy(world.goal_constr)
        for i, agent in enumerate(world.agents):
            agent.color = np.array([1, 0.95, 0.8])
            agent.state.p_vel = np.zeros(world.dim_p)
            agent_constr = random.choice(world.start_constr)
            agent.state.p_pos = np_random.uniform(*zip(*agent_constr))

            agent.goal_a = world.goals[i]
            agent.goal_a.color = np.array([0.835, 0.90, 0.831])
            agent.goal_a.state.p_vel = np.zeros(world.dim_p)
            goal_constr = random.choice(temp_goal_constr)
            agent.goal_a.state.p_pos = np_random.uniform(*zip(*goal_constr))
            temp_goal_constr.remove(goal_constr)
            
            agent.goal_b = world.goals[len(world.goals) - 1 - i]
            agent.goal_b.color = np.array([0.85, 0.90, 0.99])
            agent.goal_b.state.p_vel = np.zeros(world.dim_p)
            agent.goal_b.state.p_pos = copy.copy(agent.state.p_pos)

        return temp_goal_constr
    
    # Reset position of dynamic obstacles
    def _reset_dynamic_obstacle(self, world, obstacle, np_random, temp_dynamic_obs_constr):
        obstacle.size = 0.025
        obstacle.movable = True
        obstacle.lock = threading.Lock()
        obstacle.color = np.array([0.26, 0.32, 0.36])
        obstacle.state.p_vel = np.zeros(world.dim_p)
        dynamic_obs_constr = random.choice(temp_dynamic_obs_constr)
        obstacle.state.p_pos = np_random.uniform(*zip(*dynamic_obs_constr))
        temp_dynamic_obs_constr.remove(dynamic_obs_constr)

    # Reset position of static obstacles, taking leftover entities from goal constraints
    def _reset_static_obstacle(self, world, obstacle, np_random, temp_static_obs_constr):
        obstacle.color = np.array([0.97, 0.801, 0.8])
        obstacle.state.p_vel = np.zeros(world.dim_p)
        static_obs_constr = random.choice(temp_static_obs_constr)
        obstacle.state.p_pos = np_random.uniform(*zip(*static_obs_constr))  
        temp_static_obs_constr.remove(static_obs_constr)
    
    # Add or remove obstacles to match the number of obstacles in problem instance
    def _match_obstacles_to_instance(self, world, num_static):
        num_total_obstacles = num_static + len(world.dynamic_obstacle_constr)
        if len(world.obstacles) > num_total_obstacles:
            world.obstacles = world.obstacles[:num_total_obstacles]
        elif len(world.obstacles) < num_total_obstacles:
            additional_obstacles = [Obstacle() for _ in range(len(world.obstacles), num_total_obstacles)]
            [setattr(obstacle, 'name', f"obs_{i+len(world.obstacles)}") for i, obstacle in enumerate(additional_obstacles)]
            world.obstacles.extend(additional_obstacles)
    
    # Reset position of obstacles
    def _reset_obstacles(self, world, np_random, leftover_entities):
        temp_static_obs_constr = copy.copy(world.static_obstacle_constr)
        if world.problem_type.startswith('precision_farming'):
            temp_static_obs_constr += leftover_entities
        temp_dynamic_obs_constr = copy.copy(world.dynamic_obstacle_constr)
        
        num_dynamic_obs = len(temp_dynamic_obs_constr)        
        self._match_obstacles_to_instance(world, len(temp_static_obs_constr))

        for i, obstacle in enumerate(world.obstacles):
            if i < num_dynamic_obs:
                self._reset_dynamic_obstacle(world, obstacle, np_random, temp_dynamic_obs_constr)
                self.npc += [NPC(obstacle.state.p_pos)]
            else:
                self._reset_static_obstacle(world, obstacle, np_random, temp_static_obs_constr)
    
    # Start a thread for each dynamic obstacle
    def _start_scripted_obstacles(self, world):
        self.scripted_obstacle_running = True
        for obstacle in world.obstacles:
            if obstacle.movable:
                t = threading.Thread(target=self.run_scripted_obstacle, args=(world, obstacle))
                t.start()
                self.scripted_obstacle_threads.append(t)   
                
    def reset_world(self, world, np_random, instance_name=None):
        self.npc.clear()
        self.stop_scripted_obstacles()
        self._set_problem_instance(world, np_random, instance_name)
        leftover_entities = self._reset_agents_and_goals(world, np_random)
        self._reset_obstacles(world, np_random, leftover_entities)
        self._start_scripted_obstacles(world)
    
    # Reward given by agents to agents for reaching their respective goals
    def reward(self, agent, world):
        return 0
    
    def observation(self, agent, world):
        agent_pos = agent.state.p_pos
        agent_vel = agent.state.p_vel
        
        num_obstacles = len(world.obstacles)
        max_observable_dist = agent.max_observable_dist
        
        observed_obstacles = [np.full_like(agent_pos, max_observable_dist) for _ in range(num_obstacles)]
        observed_goal = np.full_like(agent_pos, max_observable_dist)
        
        for i, obstacle in enumerate(world.obstacles):
            if obstacle.movable:
                with obstacle.lock:
                    obs_pos = obstacle.state.p_pos
            else:
                obs_pos = obstacle.state.p_pos
            relative_pos = obs_pos - agent_pos
            dist = np.linalg.norm(relative_pos)
            if dist <= max_observable_dist:
                observed_obstacles[i] = relative_pos
                
        goal_pos = agent.goal_b.state.p_pos if agent.reached_goal else agent.goal_a.state.p_pos
        relative_goal_pos = goal_pos - agent_pos
        goal_dist = np.linalg.norm(relative_goal_pos)
        if goal_dist <= max_observable_dist:
            observed_goal = relative_goal_pos
        
        return np.concatenate((agent_pos, agent_vel, np.concatenate(observed_obstacles, axis=0), observed_goal))
            
    # Run a thread for each scripted obstacle
    def run_scripted_obstacle(self, world, obstacle):
        while self.scripted_obstacle_running:
            # self.logger.debug(f'{obstacle.name} size: {obstacle.size:}, position: {obstacle.state.p_pos}')
            action, size = self._action_callback(obstacle, world)
            obstacle.update(action, size)
            time.sleep(0.5)
        
    # disaster response: increase obstacle size to resemble increasing size of fire
    # precision farming: move obstacle in a zig-zag pattern to resemble a tractor
    def _action_callback(self, obstacle, world):
        size = None
        action = None
        instance = world.problem_instance
        if world.problem_type == 'disaster_response':
            if instance == 'instance_0':
                size = 0.005
            elif instance == 'instance_1':
                size = 0.0075
            elif instance == 'instance_2':
                size = 0.01
            elif instance == 'instance_3':
                size = 0.0125
        else:
            action = np.zeros(world.dim_p)
            obstacle_num = int(obstacle.name.split('_')[-1])
            instance_num = int(instance.split('_')[-1])
            action = self.npc[obstacle_num].get_scripted_action(obstacle, instance_num)
            sensitivity = 2.0
            action *= sensitivity

        return action, size

    # Stop all threads for scripted obstacles
    def stop_scripted_obstacles(self):
        self.scripted_obstacle_running = False
        for t in self.scripted_obstacle_threads:
            t.join()
        self.scripted_obstacle_threads.clear()
        
    # Create a logger to log information from threads
    def _add_logger(self):
        self.logger = logging.getLogger('Dynamic Obstacles')
        self.logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)

        self.logger.addHandler(ch)