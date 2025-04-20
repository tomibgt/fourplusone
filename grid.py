
class Grid:

    x_min: int = 0
    x_max: int = 0
    y_min: int = 0
    y_max: int = 0
    intersection: dict[tuple[int, int], bool] = {}

    def __init__(self):
        for i in range(3):
            self.fill(i, 0)
            self.fill(i-3, 3)
            self.fill(i+3, 3)
            self.fill(i-4, 6)
            self.fill(i+2, 6)
            self.fill(i-1, 9)
            self.fill(2, i+1)
            self.fill(-1, i)
            self.fill(5, i+4)
            self.fill(2, i+7)
            self.fill(-1, i+6)
            self.fill(-4, i+3)

    def fill(self, x: int, y: int):
        self.intersection[(x, y)] = True
        if x > self.x_max:
            self.x_max = x
        if y > self.y_max:
            self.y_max = y
        if x < self.x_min:
            self.x_min = x
        if y < self.y_min:
            self.y_min = y

    def is_filled(self, x: int, y: int):
        if (x, y) in self.intersection:
            return self.intersection[(x,y)]
        return False

