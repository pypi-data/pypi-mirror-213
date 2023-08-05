import pygame
import numpy as np
from utils.npc import NPC

pygame.init()
scale_factor = 400
window_size = (800, 800)
window = pygame.display.set_mode(window_size)

start = (0.9, 0.9)
npc = NPC(start)
scenario_num = 0

class State:
    def __init__(self, start):
        self.p_pos = np.array(start)

class Obs:
    def __init__(self, start):
        self.state = State(start)

obs = Obs(start)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    action = npc.get_scripted_action(obs, scenario_num)
    # Adjust this value to change the speed of the NPC
    obs.state.p_pos += action * 0.005

    # Draw the NPC
    window.fill((0, 0, 0))  # Clear the window

    # Draw the start point as a blue circle
    x_start, y_start = np.array(start) * scale_factor + np.array(window_size) / 2
    pygame.draw.circle(window, (0, 0, 255), (int(x_start), int(y_start)), 10)

    # Draw the destination as a red rectangle
    bounds = npc.farming_instances[scenario_num]['bounds']
    x_bounds, y_bounds = np.array(bounds) * scale_factor + np.array(window_size) / 2
    width = x_bounds[1] - x_bounds[0]
    height = y_bounds[1] - y_bounds[0]
    pygame.draw.rect(window, (255, 0, 0), pygame.Rect(x_bounds[0], y_bounds[0], width, height))

    # Convert NPC coordinates to Pygame coordinates
    x, y = obs.state.p_pos * scale_factor + np.array(window_size) / 2
    # Draw the NPC as a white circle
    pygame.draw.circle(window, (255, 255, 255), (int(x), int(y)), 10)
    pygame.display.flip()  # Update the window

pygame.quit()