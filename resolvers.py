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
        self.view.set_resolver(self)

    def is_still_going(self) -> bool:
        return self.still_going

    def make_a_move() -> bool:
        pass

class RandomResolver(Resolver):

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
        return move_made
    
class UltimateResolver(Resolver):

    infile: str  = None
    #infile: str  = "resolveIN.log"
    outfile: str = "resolveOUT.log"

    def make_a_move(self) -> bool:
        # New round begins
        moves_available: bool = False
        # If there has been a previous round, we replace the input file with the outputfile
        if os.path.exists(self.outfile):
            self.infile = "resolveIN.log"
            os.rename(self.outfile, self.infile)

        # If there is an input file, process it
        if self.infile is not None:
            with open(self.infile, "r") as f:
                previous_moves = []
                for line in f:
                    move = tuple(int(val) if val.strip() != '' else None for val in line.strip().split(","))
                    # Once we get to the end of a path, find the possible moves there and store
                    if move[0] is None:
                        if self.find_new_moves(previous_moves):
                            moves_available = True
                        else:
                            self.still_going = False
                        previous_moves = []
                    else:
                        previous_moves.append(move)
        # If there is no input file, get started
        else:
            self.find_new_moves(None)
            moves_available = True
        return moves_available

    def find_new_moves(self, previous_moves: list[(int, int, int, int)]):
        self.game_grid = Grid()

        # Initialize the grid with the previous moves
        if previous_moves is not None:
            for move in previous_moves:
                self.game_grid.add_line_to_grid(*move)
                self.view.refresh()

        # Find out the possible next moves and store them as new paths
        possible_moves: list[tuple[int, int, int, int]] = []
        for target in self.game_grid.intersections:
            x = target[0]
            y = target[1]
            if self.game_grid.is_valid_line(x, y, 1, 1): # \.
                possible_moves.append((x, y, 1, 1))
            if self.game_grid.is_valid_line(x, y, 0, 1): # |.
                possible_moves.append((x, y, 0, 1))
            if self.game_grid.is_valid_line(x, y, -1, 1): #./
                possible_moves.append((x, y, -1, 1))
            if self.game_grid.is_valid_line(x, y, -1, 0): # .–
                possible_moves.append((x, y, -1, 0))
            if self.game_grid.is_valid_line(x, y, -1, -1): # '\
                possible_moves.append((x, y, -1, -1))
            if self.game_grid.is_valid_line(x, y, 0, -1): # |'
                possible_moves.append((x, y, 0, -1))
            if self.game_grid.is_valid_line(x, y, 1, -1): # /'
                possible_moves.append((x, y, 1, -1))
            if self.game_grid.is_valid_line(x, y, 1, 0): # –.
                possible_moves.append((x, y, 1, 0))

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
    