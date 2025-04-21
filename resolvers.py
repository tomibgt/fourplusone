from grid import Grid
import random

class Resolver:

    game_grid: Grid = None

    def __init__(self, grid: Grid):
        self.game_grid = grid
        

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
