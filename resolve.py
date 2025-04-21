import pygame
from grid import Grid
from resolvers import UltimateResolver
import random
from view import View

width      = 600
height     = 400
ticker     = 0
line_count = 0

# Run the game
pygame.init()

view     = View(width, height)
resolver = UltimateResolver(view=view)

running = True

while running:

    opening = resolver.make_a_move()
    if opening:
        line_count += 1

    # Poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



    while not opening and running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

pygame.quit()

