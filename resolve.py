import pygame
from grid import Grid
from pygame.math import Vector2

width = 600
height = 400
resolution_grid = Grid()
ticker = 0

# Run the game
pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

while running:

    # Poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")

    x_scale_candidate = (width - 10) / (resolution_grid.x_max - resolution_grid.x_min)
    y_scale_candidate = (height - 10) / (resolution_grid.y_max - resolution_grid.y_min)
    scale = min(x_scale_candidate, y_scale_candidate)
    x_offset = (width - ((resolution_grid.x_max - resolution_grid.x_min) * scale) - 10) / 2
    y_offset = (height - ((resolution_grid.y_max - resolution_grid.y_min) * scale) - 10) / 2

    for x in range(resolution_grid.x_min, resolution_grid.x_max+1):
        for y in range(resolution_grid.y_min, resolution_grid.y_max+1):
            if resolution_grid.is_filled(x, y):
                pygame.draw.circle(surface=screen, 
                                    center=Vector2(((x-resolution_grid.x_min)*scale)+5+x_offset, 
                                            ((y-resolution_grid.y_min)*scale)+5+y_offset),
                                    color="black",
                                    radius=2)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60?
    ticker += 1
    #print(f"{ticker}")

pygame.quit()

