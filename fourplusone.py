import os
import sys
import argparse
import pygame
from resolvers import *
from view import View
from grid import *

def main():

    resolver: Resolver = None
    width: int         = 600 # Screen width
    height: int        = 400 # Screen height

    pygame.init()
    view     = View(width, height)

    parser = argparse.ArgumentParser(
        description="Run the four plus one solitaire."
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--random-resolve", action="store_true", help="Run a random resolution of the solitaire.")
    group.add_argument("--ultimate-resolve", action="store_true", help="Run the ultimate resolver.")

    args = parser.parse_args()

    if args.random_resolve:
        resolver = RandomResolver()
    elif args.ultimate_resolve:
        resolver = UltimateResolver()
    else:
        print("Please use one of the flags: --random-resolve, --ultimate-resolve")
        parser.print_help()
        sys.exit(1)


    resolver.set_view(view)
    view.refresh()
    #resolver = UltimateResolver(view=view)

    running = True

    while running:

        opening = resolver.add_a_line()

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

if __name__ == "__main__":
    main()
