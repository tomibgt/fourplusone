import pygame
from grid import Grid
from resolvers import UltimateResolver
from pygame.math import Vector2
import random

width      = 600
height     = 400
#resolver        = RandomResolver()
resolver   = UltimateResolver()

ticker     = 0
line_count = 0

# Run the game
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
font = pygame.font.SysFont('Arial', 10)

while running:

    opening = resolver.make_a_move()
    if opening:
        line_count += 1

    # Poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")

    x_scale_candidate = (width - 10) / (resolver.game_grid.x_max - resolver.game_grid.x_min)
    y_scale_candidate = (height - 10) / (resolver.game_grid.y_max - resolver.game_grid.y_min)
    scale = min(x_scale_candidate, y_scale_candidate)
    x_offset = (width - ((resolver.game_grid.x_max - resolver.game_grid.x_min) * scale) - 10) / 2
    y_offset = (height - ((resolver.game_grid.y_max - resolver.game_grid.y_min) * scale) - 10) / 2

    for x in range(resolver.game_grid.x_min, resolver.game_grid.x_max+1):
        for y in range(resolver.game_grid.y_min, resolver.game_grid.y_max+1):
            if resolver.game_grid.is_filled(x, y):
                pygame.draw.circle(surface=screen, 
                                    center=Vector2(((x-resolver.game_grid.x_min)*scale)+5+x_offset, 
                                            ((y-resolver.game_grid.y_min)*scale)+5+y_offset),
                                    color="black",
                                    radius=2)
                
    for segment in resolver.game_grid.line_segments.keys():
        x = segment[0]
        y = segment[1]
        x2 = segment[2]
        y2 = segment[3]
        pygame.draw.line(surface=screen,
                         color="black",
                         start_pos=Vector2(((x-resolver.game_grid.x_min)*scale)+5+x_offset, 
                                            ((y-resolver.game_grid.y_min)*scale)+5+y_offset),
                         end_pos=Vector2(((x2-resolver.game_grid.x_min)*scale)+5+x_offset, 
                                            ((y2-resolver.game_grid.y_min)*scale)+5+y_offset))

    punctuator = "!"
    if opening:
        punctuator = "..."        
    text = font.render(f'Line: {line_count}{punctuator}', True, "black")
    screen.blit(text, (1, 1))

    pygame.display.flip()

    while not opening and running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    clock.tick(60)  # limits FPS to 60?
    ticker += 1

pygame.quit()

