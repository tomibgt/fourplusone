from __future__ import annotations

class Grid:
    """This class models the grid and other elements of the 4+1 solitaire."""

    x_min: int = 0
    x_max: int = 0
    y_min: int = 0
    y_max: int = 0

    def __init__(self):
        self.line_count = 0
        self.intersections: dict[tuple[int, int], bool] = {}
        self.line_segments: dict[tuple[int, int, int, int]] = {}
        """Initialize the grid with the initial plus laid on it."""
        for i in range(3):
            self._fill_intersection(  i  ,   0  )
            self._fill_intersection(i - 3,   3  )
            self._fill_intersection(i + 3,   3  )
            self._fill_intersection(i - 4,   6  )
            self._fill_intersection(i + 2,   6  )
            self._fill_intersection(i - 1,   9  )
            self._fill_intersection(  2  , i + 1)
            self._fill_intersection( -1  ,   i  )
            self._fill_intersection(  5  , i + 4)
            self._fill_intersection(  2  , i + 7)
            self._fill_intersection( -1  , i + 6)
            self._fill_intersection( -4  , i + 3)

    def add_line_to_grid(self, x: int, y: int, x_heading: int, y_heading: int):
        """
        Add a line to the grid, starting from (x, y) and extending in the direction
        defined by (x_heading, y_heading). Each heading must be -1, 0, or 1.

        Args:
            x (int): X-coordinate of the starting point.
            y (int): Y-coordinate of the starting point.
            x_heading (int): Direction along the X-axis: -1 (left), 0 (vertical), 1 (right).
            y_heading (int): Direction along the Y-axis: -1 (up), 0 (horizontal), 1 (down).

        Raises:
            ValueError: If the heading isn't specified correctly.
        """

        if (x_heading, y_heading) not in {
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1),
            (0, 0)
        }:
            raise ValueError("x_heading and y_heading must each be -1, 0, or 1")
        
        if self.is_valid_line(x, y, x_heading, y_heading):
            for i in range(5):
                xi = x + i * x_heading
                yi = y + i * y_heading
                self._fill_intersection(xi, yi)

                if i < 4:
                    next_x = x + (i + 1) * x_heading
                    next_y = y + (i + 1) * y_heading
                    sx1, sy1, sx2, sy2 = self._normalize_segment(xi, yi, next_x, next_y)
                    self._add_line_segment(sx1, sy1, sx2, sy2)
            self.line_count += 1

    def _add_line_segment(self, x: int, y: int, x2: int, y2: int):
        """
        Adds a line segment to the grid (x, y) to (x2, y2).

        x2 should be one bigger than x, except if they are equal,
        in which case y2 should be one bigger than y.

        Args:
            x (int): X-coordinate of the starting point.
            y (int): Y-coordinate of the starting point.
            x2 (int): X-coordinate of the end point.
            y2 (int): Y-coordinate of the end point.

        Raises:
            ValueError: If the segment does not follow a valid one-unit direction.
        """
        xdiff = x2 - x
        ydiff = y2 - y
        if abs(xdiff) > 1 or abs(ydiff) > 1 or xdiff == -1 or (xdiff == 0 and ydiff != 1):
            raise ValueError("Segment should be pointed straight or diagonally rightwards or straight down.")
        self.line_segments[(x, y, x2, y2)] = True

    def _fill_intersection(self, x: int, y: int):
        """
        Mark the intersection (x, y) as filled.

        If the intersection is outside the x_min, x_max, y_min, y_max scope,
        extends the scope.

        Args:
            x (int): X-coordinate of the intersection.
            y (int): Y-coordinate of the intersection.
        """
        self.intersections[(x, y)] = True
        if x > Grid.x_max:
            Grid.x_max = x
        if y > Grid.y_max:
            Grid.y_max = y
        if x < Grid.x_min:
            Grid.x_min = x
        if y < Grid.y_min:
            Grid.y_min = y

    def _has_segment(self, x: int, y: int, x2: int, y2:int) -> bool:
        """
        Checks whether the segment from (x, y) to (x2, y2) is occupied.

        x2 should be one bigger than x, except if they are equal,
        in which case y2 should be one bigger than y.

        Args:
            x (int): X-coordinate of the starting point.
            y (int): Y-coordinate of the starting point.
            x2 (int): X-coordinate of the end point.
            y2 (int): Y-coordinate of the end point.

        Returns:
            bool: True if the segment is occupied, False otherwise.

        Raises:
            ValueError: If the segment would not follow a valid one-unit direction.
        """
        xdiff = x2 - x
        ydiff = y2 - y
        if abs(xdiff) > 1 or abs(ydiff) > 1 or xdiff == -1 or (xdiff == 0 and ydiff != 1):
            raise ValueError("Segment can only be pointed rightwards or down.")
        if(x, y, x2, y2) in self.line_segments:
            return self.line_segments[(x, y, x2, y2)]
        return False

    def is_filled(self, x: int, y: int) -> bool:
        """
        Checks if the segment (x, y) is filled.

        Args:
            x (int): X-coordinate.
            y (int): Y-coordinate.

        Returns:
            bool: True, if the coordinate is filled, False otherwise.
        """
        if (x, y) in self.intersections:
            return self.intersections[(x,y)]
        return False
    
    def is_valid_line(self, x: int, y: int, x_heading: int, y_heading: int) -> bool:
        """
        Check if a line, starting from (x, y) and heading towards
        (x_heading, y_heading) would be valid to place according to the
        game rules.

        Args:
            x (int): X-coordinate of the starting point.
            y (int): Y-coordinate of the starting point.
            x_heading (int): Direction along the X-axis: -1 (left), 0 (vertical), 1 (right).
            y_heading (int): Direction along the Y-axis: -1 (up), 0 (horizontal), 1 (down).

        Raises:
            ValueError: If the heading isn't specified correctly.
        """
        if abs(x_heading) > 1 or abs(y_heading) > 1:
            raise ValueError("x_heading and y_heading must each be -1, 0, or 1")

        filled = 0
        empty = 0
        for i in range(5):
            if self.is_filled(x + (i * x_heading), y + (i * y_heading)):
                filled += 1
            else:
                empty +=1
            if i < 4:
                sx1, sy1, sx2, sy2 = self._normalize_segment(x + (i * x_heading), y + (i * y_heading), x + ((i + 1) * x_heading), y + ((i + 1) * y_heading))
                if self._has_segment(sx1, sy1, sx2, sy2):
                    return False
        if filled != 4:
            return False
        return True

    def _normalize_segment(self, x: int, y: int, x2: int, y2: int) -> tuple[int, int, int, int]:
        """
        Normalize a line segment so that x2 is one bigger than x,
        except if they are equal, in which case y2 is one bigger than y.

        Args:
            x (int): X-coordinate of the starting point.
            y (int): Y-coordinate of the starting point.
            x2 (int): X-coordinate of the end point.
            y2 (int): Y-coordinate of the end point.

        Returns:
            tuple[int, int, int, int]: A tuple of the normalized segment coordinates.

        Raises:
            ValueError: If the given coordinate combination is incomprehendable.
        """
        if abs(x-x2) > 1 or abs(y-y2) > 1 or (x == x2 and y == y2):
            raise ValueError("The segment must be one unit long, horizontal, vertical or diagonal.")
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
