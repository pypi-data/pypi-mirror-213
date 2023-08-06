import copy
import numpy as np
import matplotlib.path as mpath

from functools import partial
from .utils.scenario import BaseScenario
from .utils.simple_env import SimpleEnv, make_env
from .utils.core import Agent, Goal, Obstacle, World
from .utils.problems import get_problem_list, get_problem_instance

from gymnasium.utils import EzPickle


class raw_env(SimpleEnv, EzPickle):
    def __init__(
        self, 
        num_agents=1, 
        num_large_obstacles=4, 
        num_small_obstacles=10, 
        render_mode=None
        ):
        
        if num_agents > 2:
            raise ValueError("Signal8 currently can only support up to 2 agents.")
        
        if num_large_obstacles > 4:
            raise ValueError("Signal8 can only support up to 4 obstacles.")
        
        scenario = Scenario()
        world = scenario.make_world(num_agents, num_large_obstacles, num_small_obstacles)
        
        super().__init__(
            scenario=scenario, 
            world=world, 
            render_mode=render_mode,
            max_cycles=500, 
        )
        
env = make_env(raw_env)

class Scenario(BaseScenario):
    def make_world(self, num_agents, num_large_obstacles, num_small_obstacles):
        world = World()
        world.problem_list = get_problem_list()

        for i in range(num_agents):
            agent = Agent()
            agent.name = f"agent_{i}"
            agent.collide = True
            agent.color = np.array([1, 0.95, 0.8])
            world.agents.append(agent)
        
        # Agents has two goals (i.e., actual goal and start position)
        # This is to ensure agent returns safely to start position after reaching goal
        for i in range(num_agents*2):
            goal = Goal()
            goal.name = f"goal_{i}"
            goal.collide = False
            # goal_a is the actual goal
            if i < num_agents:
                goal.color = np.array([0.835, 0.90, 0.831])
            # goal_b is the start position to return to after reaching goal
            else:
                goal.color = np.array([0.85, 0.90, 0.99])
            world.goals.append(goal)
        
        # Large obstacles can only be observed by aerial agent
        for i in range(num_large_obstacles):
            obstacle = Obstacle(size=0.1)
            obstacle.name = f"obs_{i}"
            obstacle.color = np.array([0.97, 0.801, 0.8])
            world.large_obstacles.append(obstacle)
        
        # Small obstacles can only be observed by ground agent(s)
        for i in range(num_small_obstacles):
            obstacle = Obstacle(size=0.01)
            obstacle.name = f"obs_{i}"
            obstacle.color = np.array([0.97, 0.801, 0.8])
            world.small_obstacles.append(obstacle)    
        
        world.buffer_dist = world.agents[0].size + world.large_obstacles[0].size
        return world
    
    # Get constraints on entities given problem instance name
    def _set_problem_instance(self, world, instance_name):
        instance_constr = get_problem_instance(instance_name)
        world.problem_instance = instance_name
        world.instance_constr = instance_constr
    
    # Generate valid points according to some condition
    def _generate_position(self, np_random, condition):
        while True:
            point = np_random.uniform(-1, +1, 2)
            if condition(point):
                break
        return point
    
    # Check if point is outside of rectangular obstacle regions
    def _safe_position(self, point, epsilon, x_constraints, y_constraints):
        return all(not (low - epsilon <= point[0] <= high + epsilon) for low, high in x_constraints) \
            and all(not (low - epsilon <= point[1] <= high + epsilon) for low, high in y_constraints)

    # Check if point is outside of triangular obstacle regions
    def _outside_triangle(self, point, paths, epsilon):
        enlarged_paths = []
        for path in paths:
            centroid = np.mean(path.vertices[:-1], axis=0)
            enlarged_vertices = path.vertices + epsilon * (path.vertices - centroid)
            enlarged_paths.append(mpath.Path(enlarged_vertices))
        return not any(path.contains_points(point[None, :]) for path in enlarged_paths)
    
    # Reset agents and goals to their initial positions
    def _reset_agents_and_goals(self, world, np_random, paths):
        epsilon = world.buffer_dist
        
        if paths is None:
            x_constraints = [constr[0] for constr in world.instance_constr]
            y_constraints = [constr[1] for constr in world.instance_constr]

        for i, agent in enumerate(world.agents):
            agent.goal_a = world.goals[i]
            agent.goal_b = world.goals[len(world.goals) - 1 - i]

            agent.state.p_vel = np.zeros(world.dim_p)
            agent.goal_a.state.p_vel = np.zeros(world.dim_p)
            agent.goal_b.state.p_vel = np.zeros(world.dim_p)

            if world.problem_instance == 'corners':
                condition = partial(
                    self._outside_triangle, 
                    paths=paths, 
                    epsilon=epsilon
                    )
            else:
                condition = partial(
                    self._safe_position, 
                    epsilon=epsilon, 
                    x_constraints=x_constraints, 
                    y_constraints=y_constraints
                    )

            agent.state.p_pos = self._generate_position(np_random, condition)
            agent.goal_a.state.p_pos = self._generate_position(np_random, condition)
            agent.goal_b.state.p_pos = copy.copy(agent.state.p_pos)
    
    # Reset all large obstacles to a position that does not intersect with the agents
    def _reset_large_obstacles(self, world, np_random, paths):
        def inside_triangle_condition(point):
            return any(path.contains_points(point[None, :]) for path in paths)
                
        occupied_triangles = set()
        for i, large_obstacle in enumerate(world.large_obstacles):            
            large_obstacle.state.p_vel = np.zeros(world.dim_p)
            idx = i % len(world.instance_constr)
            
            # Each corner may only have one large_obstacle in it
            if world.problem_instance == 'corners':
                while True:
                    pos = self._generate_position(np_random, inside_triangle_condition)
                    triangle_idx = next((i for i, path in enumerate(paths) if path.contains_points(pos[None, :])), None)
                    if triangle_idx not in occupied_triangles:
                        large_obstacle.state.p_pos = pos
                        occupied_triangles.add(triangle_idx)
                        break
            else:                
                large_obstacle.state.p_pos = np_random.uniform(*zip(*world.instance_constr[idx]))
    
    # Reset all small obstacles to a position that does not intersect with the agents or the large obstacles
    def _reset_small_obstacles(self, world, np_random, paths):
        epsilon = world.small_obstacles[0].size + world.large_obstacles[0].size
        
        x_constraints = [constr[0] for constr in world.instance_constr]
        y_constraints = [constr[1] for constr in world.instance_constr]
        agent_positions = [agent.state.p_pos for agent in world.agents]
        goal_positions = [goal.state.p_pos for goal in world.goals]
        large_obstacle_positions = [obstacle.state.p_pos for obstacle in world.large_obstacles]
        
        def safe_position(point):
            if world.problem_instance == 'corners':
                within_obstacle_constraints = any(path.contains_points(point[None, :]) for path in paths)
            else:
                within_obstacle_constraints = any(low - epsilon <= point[0] <= high + epsilon for low, high in x_constraints) \
                    or any(low - epsilon <= point[1] <= high + epsilon for low, high in y_constraints)

            within_other_positions = any(np.linalg.norm(point - pos) <= epsilon for pos in agent_positions + goal_positions + large_obstacle_positions)

            return not (within_obstacle_constraints or within_other_positions)
        
        for small_obstacle in world.small_obstacles:
            small_obstacle.state.p_vel = np.zeros(world.dim_p)
            small_obstacle.state.p_pos = self._generate_position(np_random, safe_position)

    def reset_world(self, world, np_random, problem_instance):
        self._set_problem_instance(world, problem_instance)
        
        paths = [mpath.Path(np.array(triangle)) for triangle in world.instance_constr] \
            if world.problem_instance == 'corners' else None
            
        self._reset_agents_and_goals(world, np_random, paths)
        self._reset_large_obstacles(world, np_random, paths)
        self._reset_small_obstacles(world, np_random, paths)
    
    # Reward given by agents to agents for reaching their respective goals
    def reward(self, agent, world):
        return 0
    
    # Ground agents can only observe the positions of other agents, goals, and small obstacles
    def observation(self, agent, world):
        agent_pos = agent.state.p_pos
        agent_vel = agent.state.p_vel
        
        num_agents = len(world.agents)
        num_small_obstacles = len(world.small_obstacles)
        max_observable_dist = agent.max_observable_dist
        
        observed_agents = [np.full_like(agent_pos, max_observable_dist) for _ in range(num_agents - 1)]
        observed_goal = np.full_like(agent_pos, max_observable_dist)
        observed_obstacles = [np.full_like(agent_pos, max_observable_dist) for _ in range(num_small_obstacles)]
        
        idx = 0
        for other_agent in world.agents:
            if agent.name == other_agent.name:
                continue
            else:
                other_agent_pos = other_agent.state.p_pos
                relative_pos = other_agent_pos - agent_pos
                dist = np.linalg.norm(relative_pos)
                if dist <= max_observable_dist:
                    observed_agents[idx] = relative_pos
                idx += 1
        
        for i, small_obstacle in enumerate(world.small_obstacles):
            obs_pos = small_obstacle.state.p_pos
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