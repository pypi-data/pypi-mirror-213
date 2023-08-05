import numpy as np


class EntityState:  # physical/external base state of all entities
    def __init__(self):
        # physical position
        self.p_pos = None
        # physical velocity
        self.p_vel = None


class AgentState(EntityState):  # state of agents
    def __init__(self):
        super().__init__()


class Entity:  # properties and state of physical world entity
    def __init__(self):
        # name
        self.name = ""
        # properties:
        self.size = 0.1
        # entity can move / be pushed
        self.movable = False
        # entity collides with others
        self.collide = True
        # color
        self.color = None
        # state
        self.state = EntityState()
        # mass
        self.initial_mass = 1.0

    @property
    def mass(self):
        return self.initial_mass


class Goal(Entity): # properties of goal entities
    def __init__(self):
        super().__init__()


class Obstacle(Entity):  # properties of obstacles entities
    def __init__(self):
        super().__init__()
        # entity can be moved / pushed
        self.movable = False
        # script behavior to execute
        self.action_callback = None
        self.lock = None
    
    # updates the state of the obstacle
    def update(self, action=None, size=None, dt=0.1, damping=0.25):
        with self.lock:
            if action is not None:
                self.state.p_vel = self.state.p_vel * (1 - damping)
                self.state.p_vel += (action / self.mass) * dt
                self.state.p_pos += self.state.p_vel * dt
            elif size is not None:
                self.size += size
            else:
                raise ValueError("Either action or size must be specified")
        

class Agent(Entity):  # properties of agent entities
    def __init__(self):
        super().__init__()
        # agents are movable by default
        self.movable = True
        # reached goal state
        self.goal_a = None
        self.reached_goal = False
        # reached start state after reaching goal
        self.goal_b = None
        self.returned_to_safety = False
        # state
        self.state = AgentState()
        # action
        self.action = None
        # how far the agent can see
        self.max_observable_dist = 0.30

class World:  # multi-agent world
    def __init__(self):
        # list of agents and entities (can change at execution-time!)
        self.agents = []
        self.goals = []
        self.obstacles = []
        # position dimensionality
        self.dim_p = 2
        # color dimensionality
        self.dim_color = 3
        # simulation timestep
        self.dt = 0.1
        # physical damping
        self.damping = 0.25
        # contact response parameters
        self.contact_force = 1e2
        self.contact_margin = 1e-3
        self.problem_type = None
        self.problem_instance = None
        self.start_constr = None
        self.goal_constr = None
        self.static_obstacle_constr = None
        self.dynamic_obstacle_constr = None
        
    # return all entities in the world
    @property
    def entities(self):
        return self.agents + self.goals + self.obstacles

    # update state of the world
    def step(self):
        # gather forces applied to entities
        p_force = [None] * len(self.entities)
        # apply agent physical controls
        p_force = self.apply_action_force(p_force)
        # apply environment forces
        p_force = self.apply_environment_force(p_force)
        # integrate physical state
        self.integrate_state(p_force)

    # gather agent action forces
    def apply_action_force(self, p_force):
        # set applied forces
        for i, agent in enumerate(self.agents):
            if agent.movable:
                p_force[i] = agent.action
        return p_force

    # gather physical forces acting on agents
    def apply_environment_force(self, p_force):
        # simple (but inefficient) collision response
        for a, agent_a in enumerate(self.agents):
            for b, agent_b in enumerate(self.agents):
                if b <= a:
                    continue
                [f_a, f_b] = self.get_collision_force(agent_a, agent_b)
                if f_a is not None:
                    if p_force[a] is None:
                        p_force[a] = 0.0
                    p_force[a] = f_a + p_force[a]
                if f_b is not None:
                    if p_force[b] is None:
                        p_force[b] = 0.0
                    p_force[b] = f_b + p_force[b]
        return p_force

    # integrate physical state
    def integrate_state(self, p_force):
        for i, agent in enumerate(self.agents):
            agent.state.p_vel = agent.state.p_vel * (1 - self.damping)
            if p_force[i] is not None:
                agent.state.p_vel += (p_force[i] / agent.mass) * self.dt
            agent.state.p_pos += agent.state.p_vel * self.dt

    # get collision forces for any contact between two agents
    def get_collision_force(self, agent_a, agent_b):
        if (not agent_a.collide) or (not agent_b.collide):
            return [None, None]  # not a collider
        if agent_a is agent_b:
            return [None, None]  # don't collide against itself
        # compute actual distance between entities
        delta_pos = agent_a.state.p_pos - agent_b.state.p_pos
        dist = np.sqrt(np.sum(np.square(delta_pos)))
        # minimum allowable distance
        dist_min = agent_a.size + agent_b.size
        # softmax penetration
        k = self.contact_margin
        penetration = np.logaddexp(0, -(dist - dist_min) / k) * k
        force = self.contact_force * delta_pos / dist * penetration
        force_a = +force if agent_a.movable else None
        force_b = -force if agent_b.movable else None
        return [force_a, force_b]