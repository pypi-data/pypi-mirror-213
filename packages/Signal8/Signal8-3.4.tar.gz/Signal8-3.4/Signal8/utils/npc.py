import numpy as np

class NPC:
    def __init__(self, start_pos):
        self.start = start_pos
        self.direction = [None, None]
        self.status = 'moving_to_destination'
        self.farming_instances = {
            0: {'destination': (-0.9, -0.9), 'direction': [-1, 1], 'bounds': [(-1, -0.4), (-1, 1)]},
            1: {'destination': (0.9, 0.9), 'direction': [-1, -1], 'bounds': [(-1, 1), (0.4, 1)]},
            2: {'destination': (0, 1), 'direction': [1, -1], 'bounds': [(-0.25, 0.25), (-1, 1)]},
            3: {'destination': (-0.75, -0.90), 'direction': [1, 1], 'bounds': [(-1, 1), (-1, -0.4)]},
        }
    
    def get_scripted_action(self, obstacle, instance_num):
        destination = self.farming_instances[instance_num]['destination']
        direction = self.farming_instances[instance_num]['direction']
        bounds = self.farming_instances[instance_num]['bounds']
        
        action = np.array([0, 0])
        with obstacle.lock:
            x, y, = obstacle.state.p_pos
        
        if self.status == 'moving_to_destination':
            if np.allclose([x, y], destination, atol=0.05):
                self.status = 'zigzagging'
                self.direction = direction
            else:
                action = self._move_towards_point(x, y, destination)
        elif self.status == 'zigzagging':
            if self.direction[1] == 1 and y > bounds[1][1] or self.direction[1] == -1 and y < bounds[1][0]:
                self.status = 'moving_to_start'
            else:
                action = self._zigzag(x, y, bounds)
        elif self.status == 'moving_to_start':
            if np.allclose([x, y], self.start, atol=0.05):
                self.status = 'moving_to_destination'
            else:
                action = self._move_towards_point(x, y, self.start)

        return action
    
    def _move_towards_point(self, x, y, point):
        x_direction = np.array(point) - np.array([x, y])
        direction_norm = x_direction / np.linalg.norm(x_direction)
        return np.round(direction_norm).astype(int)

    def _within_bounds(self, x, y, bounds):
        x_bounds, y_bounds = bounds
        return x_bounds[0] <= x <= x_bounds[1] and y_bounds[0] <= y <= y_bounds[1]

    def _zigzag(self, x, y, bounds):
            if self.direction[0] == 1:
                if x < bounds[0][1]:
                    return np.array([1, 0])
                else:
                    self.direction[0] = -1 
                    return np.array([0, self.direction[1]])
            elif self.direction[0] == -1:
                if x > bounds[0][0]:
                    return np.array([-1, 0])
                else:
                    self.direction[0] = 1
                    return np.array([0, self.direction[1]])