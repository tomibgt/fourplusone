
class Grid:

    x_min: int = 0
    x_max: int = 0
    y_min: int = 0
    y_max: int = 0
    intersection: dict[tuple[int, int], bool] = {}
    line_segment: dict[tuple[int, int, int, int]] = {}

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

    def add_line(self, x: int, y: int, x_heading: int, y_heading: int):
        if self.is_valid_line(x, y, x_heading, y_heading):
            for i in range(5):
                self.fill(x + (i * x_heading), y + (i * y_heading))
                if i < 4:
                    sx1, sy1, sx2, sy2 = self.normalize_segment(x + (i * x_heading), y + (i * y_heading), x + ((i + 1) * x_heading), y + ((i + 1) * y_heading))
                    self.add_line_segment(sx1, sy1, sx2, sy2)

    def add_line_segment(self, x: int, y: int, x2: int, y2: int):
        self.line_segment[(x, y, x2, y2)] = True

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

    def has_segment(self, x: int, y: int, x2: int, y2:int):
        if(x, y, x2, y2) in self.line_segment:
            return self.line_segment[(x, y, x2, y2)]
        return False


    def is_filled(self, x: int, y: int):
        if (x, y) in self.intersection:
            return self.intersection[(x,y)]
        return False
    
    def is_valid_line(self, x: int, y: int, x_heading: int, y_heading: int):
        filled = 0
        empty = 0
        for i in range(5):
            if self.is_filled(x + (i * x_heading), y + (i * y_heading)):
                filled += 1
            else:
                empty +=1
            if i < 4:
                sx1, sy1, sx2, sy2 = self.normalize_segment(x + (i * x_heading), y + (i * y_heading), x + ((i + 1) * x_heading), y + ((i + 1) * y_heading))
                if self.has_segment(sx1, sy1, sx2, sy2):
                    return False
        if filled != 4:
            return False
        return True

    def normalize_segment(self, x: int, y: int, x2: int, y2: int):
        ret_x = x
        ret_y = y
        ret_x2 = x2
        ret_y2 = y2
        if x > x2 or (x == x2 and y > y2):
            ret_x = x2
            ret_x2 = x
            ret_y = y2
            ret_y2 = y
        return ret_x, ret_y, ret_x2, ret_y2
