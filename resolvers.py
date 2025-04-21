from __future__ import annotations

import random
import os
import pygame

from grid import Grid
from view import View

class Resolver:

    game_grid: Grid = None

    def __init__(self, grid: Grid = None, view: View = None):
        if grid is None:
            grid = Grid()
        self.game_grid   = grid
        self.still_going = True
        self.view        = view
        if self.view is not None:
            self.view.set_resolver(self)

    def is_still_going(self) -> bool:
        return self.still_going

    def make_a_move() -> bool:
        pass

    def set_view(self, view: View):
        self.view = view
        self.view.set_resolver(self)

class RandomResolver(Resolver):

    def __init__(self):
        super().__init__()
        self.clock = pygame.time.Clock()

    def make_a_move(self) -> bool:
        opening   = True
        move_made = False
        x = None
        y = None
        x2 = None
        y2 = None
        while opening and not move_made:
            opening = False
            for target in self.game_grid.intersections:
                x = target[0]
                y = target[1]
                if self.game_grid.is_valid_line(x, y, 0, -1):
                    opening = True
                    x2 = 0
                    y2 = -1
                    if random.choice([True, False]):
                        break
                if self.game_grid.is_valid_line(x, y, 1, -1):
                    opening = True
                    x2 = 1
                    y2 = -1
                    if random.choice([True, False]):
                        break
                if self.game_grid.is_valid_line(x, y, 1, 0):
                    opening = True
                    x2 = 1
                    y2 = 0
                    if random.choice([True, False]):
                        break
                if self.game_grid.is_valid_line(x, y, 1, 1):
                    opening = True
                    x2 = 1
                    y2 = 1
                    if random.choice([True, False]):
                        break
                if self.game_grid.is_valid_line(x, y, 0, 1):
                    opening = True
                    x2 = 0
                    y2 = 1
                    if random.choice([True, False]):
                        break
                if self.game_grid.is_valid_line(x, y, -1, 1):
                    opening = True
                    x2 = -1
                    y2 = 1
                    if random.choice([True, False]):
                        break
                if self.game_grid.is_valid_line(x, y, -1, 0):
                    opening = True
                    x2 = -1
                    y2 = 0
                    if random.choice([True, False]):
                        break
                if self.game_grid.is_valid_line(x, y, -1, -1):
                    opening = True
                    x2 = -1
                    y2 = -1
                    if random.choice([True, False]):
                        break
            if x2 is not None:
                self.game_grid.add_line_to_grid(x, y, x2, y2)
                move_made = True
            self.still_going = move_made
            self.clock.tick(2)
            self.view.refresh()
        return move_made
    
class UltimateResolver(Resolver):

    infile: str  = None
    #infile: str  = "resolveIN.log"
    outfile: str = "resolveOUT.log"
    current_path: int = 0
    total_paths: int  = 0
    future_paths: int = 0
    ticker: int       = 1

    def make_a_move(self) -> bool:
        """
        Loads the stored movement paths from the input file and requests for
        storing newly found movement paths to the output file.

        Returns:
            bool: True if there is still paths to be processed. False otherwise.
        """
        # New round begins
        moves_available: bool = False
        # If there has been a previous round, we replace the input file with the outputfile
        if os.path.exists(self.outfile):
            self.infile = "resolveIN.log"
            os.rename(self.outfile, self.infile)

        # If there is an input file, process it
        self.total_paths = self.future_paths
        self.future_paths = 1 # Counter for how many new paths have been stored in the output file
        self.current_path = 1 # Counter for how many paths have been processed from the input file
        if self.infile is not None:
            with open(self.infile, "r") as file_handle:
                previous_moves = []
                for line in file_handle:
                    game_move = tuple(int(val) if val.strip() != '' else None for val in line.strip().split(","))
                    # Once we get to the end of a path, find the possible moves there and store
                    if game_move[0] is None:
                        self.current_path += 1
                        if self.find_new_moves(previous_moves):
                            moves_available = True
                        else:
                            self.still_going = False
                        previous_moves = []
                    else:
                        previous_moves.append(game_move)
        # If there is no input file, get started with new files
        else:
            self.find_new_moves(None)
            moves_available = True
        self.view.refresh()

        return moves_available

    def find_new_moves(self, previous_moves: list[(int, int, int, int)]):
        """
        Should be fed a previously traversed path of line adding moves.
        Produces all possibly lines that could be played as a next move.
        Stores in the output file new paths that each consist of the
        previous moves path, added with one of the new options.

        Args:
            previous_moves (list[(int, int, int, int)]) List of tuples (x, y, h_heading, y_heading) with a line start coordinate (x,y) and -1, 0, +1 headings
        """

        # Get a fresh grid
        self.game_grid = Grid()

        # Initialize the grid with making the previous moves
        if previous_moves is not None:
            for move in previous_moves:
                self.game_grid.add_line_to_grid(*move)
                self.view.refresh()

        # Find out the possible next moves and store them as new paths
        possible_moves: list[tuple[int, int, int, int]] = []
        for target in self.game_grid.intersections:
            x = target[0]
            y = target[1]
            Grid.focus = [x, y] # Tell the viewer what intersection are we interested in now
            self.ticker += 1
            if self.ticker > 3:
                self.view.refresh()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                self.ticker = 1
            if self.game_grid.is_valid_line(x, y, 1, 1): # \.
                possible_moves.append((x, y, 1, 1))
                self.future_paths += 1
            if self.game_grid.is_valid_line(x, y, 0, 1): # |.
                possible_moves.append((x, y, 0, 1))
                self.future_paths += 1
            if self.game_grid.is_valid_line(x, y, -1, 1): #./
                possible_moves.append((x, y, -1, 1))
                self.future_paths += 1
            if self.game_grid.is_valid_line(x, y, -1, 0): # .–
                possible_moves.append((x, y, -1, 0))
                self.future_paths += 1
            if self.game_grid.is_valid_line(x, y, -1, -1): # '\
                possible_moves.append((x, y, -1, -1))
                self.future_paths += 1
            if self.game_grid.is_valid_line(x, y, 0, -1): # |'
                possible_moves.append((x, y, 0, -1))
                self.future_paths += 1
            if self.game_grid.is_valid_line(x, y, 1, -1): # /'
                possible_moves.append((x, y, 1, -1))
                self.future_paths += 1
            if self.game_grid.is_valid_line(x, y, 1, 0): # –.
                possible_moves.append((x, y, 1, 0))
                self.future_paths += 1

        # Store each possible move in the outfile, preceeded by the path so far
        with open(self.outfile, "a") as outputfile:
            for move in possible_moves:
                if previous_moves is not None:
                    for previous_move in previous_moves:
                        outputfile.write(",".join(map(str, previous_move)) + "\n")
                outputfile.write(",".join(map(str, move)) + "\n")
                outputfile.write(",,,\n")
                outputfile.flush()
        return len(possible_moves) > 0
    