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

    x = None
    y = None
    x2 = None
    y2 = None
    for target in resolution_grid.intersection:
        x = target[0]
        y = target[1]
        if resolution_grid.is_valid_line(x, y, 0, -1):
            x2 = 0
            y2 = -1
            break
        if resolution_grid.is_valid_line(x, y, 1, -1):
            x2 = 1
            y2 = -1
            break
        if resolution_grid.is_valid_line(x, y, 1, 0):
            x2 = 1
            y2 = 0
            break
        if resolution_grid.is_valid_line(x, y, 1, 1):
            x2 = 1
            y2 = 1
            break
        if resolution_grid.is_valid_line(x, y, 0, 1):
            x2 = 0
            y2 = 1
            break
        if resolution_grid.is_valid_line(x, y, -1, 1):
            x2 = -1
            y2 = 1
            break
        if resolution_grid.is_valid_line(x, y, -1, 0):
            x2 = -1
            y2 = 0
            break
        if resolution_grid.is_valid_line(x, y, -1, -1):
            x2 = -1
            y2 = -1
            break
    if x2 is not None:
        resolution_grid.add_line(x, y, x2, y2)

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
                
    for segment in resolution_grid.line_segment.keys():
        x = segment[0]
        y = segment[1]
        x2 = segment[2]
        y2 = segment[3]
        pygame.draw.line(surface=screen,
                         color="black",
                         start_pos=Vector2(((x-resolution_grid.x_min)*scale)+5+x_offset, 
                                            ((y-resolution_grid.y_min)*scale)+5+y_offset),
                         end_pos=Vector2(((x2-resolution_grid.x_min)*scale)+5+x_offset, 
                                            ((y2-resolution_grid.y_min)*scale)+5+y_offset))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60?
    ticker += 1
    #print(f"{ticker}")

pygame.quit()

