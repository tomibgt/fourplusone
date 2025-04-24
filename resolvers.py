from __future__ import annotations
from datetime import datetime, timedelta
import json
import random
import os
import sys
import pygame

from grid import *
from view import View

class Resolver:

    #game_grid: Grid = None

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

    def add_a_line() -> bool:
        pass

    def set_view(self, view: View):
        self.view = view
        self.view.set_resolver(self)

class RandomResolver(Resolver):

    def __init__(self):
        super().__init__()
        self.game_grid   = Grid()
        self.clock = pygame.time.Clock()

    def add_a_line(self) -> bool:
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
                if self.game_grid.is_valid_line(Line(x, y, 0, -1)):
                    opening = True
                    x2 = 0
                    y2 = -1
                    if random.choice([True, False]):
                        break
                if self.game_grid.is_valid_line(Line(x, y, 1, -1)):
                    opening = True
                    x2 = 1
                    y2 = -1
                    if random.choice([True, False]):
                        break
                if self.game_grid.is_valid_line(Line(x, y, 1, 0)):
                    opening = True
                    x2 = 1
                    y2 = 0
                    if random.choice([True, False]):
                        break
                if self.game_grid.is_valid_line(Line(x, y, 1, 1)):
                    opening = True
                    x2 = 1
                    y2 = 1
                    if random.choice([True, False]):
                        break
                if self.game_grid.is_valid_line(Line(x, y, 0, 1)):
                    opening = True
                    x2 = 0
                    y2 = 1
                    if random.choice([True, False]):
                        break
                if self.game_grid.is_valid_line(Line(x, y, -1, 1)):
                    opening = True
                    x2 = -1
                    y2 = 1
                    if random.choice([True, False]):
                        break
                if self.game_grid.is_valid_line(Line(x, y, -1, 0)):
                    opening = True
                    x2 = -1
                    y2 = 0
                    if random.choice([True, False]):
                        break
                if self.game_grid.is_valid_line(Line(x, y, -1, -1)):
                    opening = True
                    x2 = -1
                    y2 = -1
                    if random.choice([True, False]):
                        break
            if x2 is not None:
                line: Line = Line(x, y, x2, y2)
                self.game_grid.add_line_to_grid(line)
                move_made = True
            self.still_going = move_made
            self.clock.tick(2)
            self.view.refresh()
        return move_made
    
class UltimateResolver(Resolver):

    infile: str   = None
    #infile: str  = "resolveIN.log"
    outfile: str  = "resolveOUT.log"
    tempfile: str = "resolveTEMP.log"
    metafile: str = "resolveDATA.log"

    def __init__(self):
        super().__init__()
        self.current_path: int   = 0
        self.total_paths: int    = 0
        self.future_paths: int   = 0
        self.ticker: int         = 1
        self.starttime: datetime = datetime.now()
        self.elapsed: timedelta  = self.starttime - self.starttime
        if os.path.exists(self.metafile):
            with open(self.metafile, "r") as metafile:
                data = json.load(metafile)
                self.elapsed = timedelta(seconds=data["elapsed"])
                self.current_path = int(data["current_path"])
                self.total_paths = int(data["total_paths"])
                self.future_paths = int(data["future_paths"])



    def add_a_line(self) -> bool:
        """
        Loads the stored movement paths from the input file and requests for
        storing newly found movement paths to the output file.

        Returns:
            bool: True if there is still paths to be processed. False otherwise.
        """
        # New round begins
        lines_available: bool = False
        # If there has been a previous round, we replace the input file with the outputfile
        if os.path.exists(self.outfile):
            self.infile = "resolveIN.log"
            os.rename(self.outfile, self.infile)

        # If there is an input file, process it
        self.total_paths = self.future_paths
        self.future_paths = 1 # Counter for how many new paths have been stored in the output file
        self.current_path = 1 # Counter for how many paths have been processed from the input file
        if self.infile is not None:
            with open(self.infile, "r") as self.file_handle:
                previous_lines = []
                for line in self.file_handle:
                    x, y, x_heading, y_heading = line.strip().split(",")
                    if x != "":
                        #stored_line = Line(int(val) if val.strip() != '' else None for val in line.strip().split(","))
                        stored_line = Line(int(x), int(y), int(x_heading), int(y_heading))
                        previous_lines.append(stored_line)
                    else:
                        self.current_path += 1
                        if self.find_new_lines(previous_lines):
                            lines_available = True
                        else:
                            self.still_going = False
                        previous_lines = []
        # If there is no input file, get started with new files
        else:
            self.find_new_lines(None)
            lines_available = True
        self.view.refresh()

        if not lines_available:
            self.stop_time: datetime = datetime.now()
            elapsed_time = self.stop_time - self.starttime
            print("Calculation complete!")
            print(f"Time used: {elapsed_time}")

        return lines_available

    def find_new_lines(self, previous_moves: list[Line]):
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
            for line in previous_moves:
                self.game_grid.add_line_to_grid(line)
                self.view.refresh()

        # Find out the possible next moves and store them as new paths
        possible_moves: list[Line] = []
        for target in self.game_grid.intersections:
            x = target[0]
            y = target[1]
            Grid.focus = [x, y] # Tell the viewer what intersection are we interested in now
            self.ticker += 1
            if self.ticker > 3:
                self.view.refresh()
                self.ticker = 1
            line_candidates = [
                Line(x, y, 1, 1),
                Line(x, y, 0, 1),
                Line(x, y, -1, 1),
                Line(x, y, -1, 0),
                Line(x, y, -1, -1),
                Line(x, y, 0, -1),
                Line(x, y, 1, -1),
                Line(x, y, 1, 0)
            ]
            for line in line_candidates:
                line.normalize()
                if self.game_grid.is_valid_line(line) and line not in possible_moves:
                    possible_moves.append(line)
                    self.future_paths += 1

        # Store each possible move in the outfile, preceeded by the path so far
        with open(self.outfile, "a") as outputfile:
            for move in possible_moves:
                if previous_moves is not None:
                    for previous_move in previous_moves:
                        outputfile.write(f"{previous_move.x},{previous_move.y},{previous_move.x_heading},{previous_move.y_heading}\n")
                outputfile.write(f"{move.x},{move.y},{move.x_heading},{move.y_heading}\n")
                outputfile.write(",,,\n")
                outputfile.flush()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.shut_down_procedure()

        return len(possible_moves) > 0
    
    def shut_down_procedure(self):
        self.stop_time: datetime = datetime.now()
        elapsed = self.stop_time - self.starttime
        with open(self.tempfile, "w") as tempfile:
            for line in self.file_handle:
                tempfile.write(f"{line}")
            self.file_handle.close()
            with open(self.outfile, "r") as outputfile:
                for line in outputfile:
                    tempfile.write(f"{line}")
            tempfile.flush()
        os.rename(self.tempfile, self.outfile)
        with open(self.metafile, "w") as metafile:
            data = {
                "elapsed": (elapsed+self.elapsed).total_seconds(),
                "current_path": self.current_path,
                "total_paths": self.total_paths,
                "future_paths": self.future_paths
            }
            json.dump(data, metafile, indent=4)
            metafile.flush()
        print("Stopping processing.")
        print(f"Processed for {elapsed} this session.")
        print(f"Altogehter processed for {elapsed+self.elapsed}")
        pygame.quit()
        sys.exit()
