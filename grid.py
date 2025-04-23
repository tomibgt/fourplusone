from __future__ import annotations
from collections import namedtuple
import bisect

class LineSegment:

    def __init__(self, x: int, y: int, x_heading: int, y_heading: int):

        if (x_heading, y_heading) not in {
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        }:
            raise ValueError("x_heading and y_heading must each be -1, 0, or 1")

        self.x: int = x
        self.y: int = y
        self.x_heading: int = x_heading
        self.y_heading: int = y_heading

    def __lt__(self, other):
        if not isinstance(other, LineSegment):
            return NotImplemented
        if self.x < other.x:
            return True
        if self.y < other.y:
            return True
        if self.x_heading < other.x_heading:
            return True
        if self.y_heading < other.y_heading:
            return True
        return False

    def __le__(self, other):
        if not isinstance(other, LineSegment):
            return NotImplemented
        if self.__lt__(other) or self.__eq__(other):
            return True
        return False

    def __eq__(self, other):
        if not isinstance(other, LineSegment):
            return NotImplemented
        return (self.x, self.y, self.x_heading, self.y_heading) == \
               (other.x, other.y, other.x_heading, other.y_heading)

    def __ne__(self, other):
        if not isinstance(other, LineSegment):
            return NotImplemented
        return (self.x, self.y, self.x_heading, self.y_heading) != \
               (other.x, other.y, other.x_heading, other.y_heading)

    def __gt__(self, other):
        if not isinstance(other, LineSegment):
            return NotImplemented
        return not self.__le__(other)

    def __ge__(self, other):
        if not isinstance(other, LineSegment):
            return NotImplemented
        return not self.__lt__(other)
    
    def __hash__(self):
        return hash((self.x, self.y, self.x_heading, self.y_heading))
    
    def __str__(self):
        return f"({self.x}, {self.y}: {self.x_heading}, {self.y_heading})"

    def __repr__(self):
        return f"({self.x}, {self.y}: {self.x_heading}, {self.y_heading})"

    def normalize(self):
        """
        Normalize this line so that x_heading is 1, with the exception of
        it being 0, in which case y_heading must be 1.

        Args:
            x (int): X-coordinate of the starting point.
            y (int): Y-coordinate of the starting point.
            x2 (int): X-coordinate of the end point.
            y2 (int): Y-coordinate of the end point.
        """
        if self.x_heading == -1:
            self.x_heading = 1
            self.x -= 1
            if self.y_heading == -1:
                self.y_heading = 1
                self.y -= 1
            elif self.y_heading == 1:
                self.y_heading = -1
                self.y += 1
        elif self.x_heading == 0 and self.y_heading == -1:
            self.y_heading = 1
            self.y -= 1

class Line:

    Point = namedtuple('Point', ['x', 'y'])

    def __init__(self, x: int, y: int, x_heading: int, y_heading: int):
        if (x_heading, y_heading) not in {
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        }:
            raise ValueError("x_heading and y_heading must each be -1, 0, or 1")
        
        self.x: int = x
        self.y: int = y
        self.x_heading: int = x_heading
        self.y_heading: int = y_heading

    def get_intersections(self):
        return [self.Point(self.x + i * self.x_heading, self.y + i * self.y_heading) for i in range(5)]

    def get_segments(self):
        """
        Returns the line segments that compose this line.

        Returns:
            list[LineSegment]: The list of normalized segments.
        """
        reva: list[LineSegment] = []
        x = self.x
        y = self.y
        for i in range(4):
            segment = LineSegment(x, y, self.x_heading, self.y_heading)
            segment.normalize()
            reva.append(segment)
            x += self.x_heading
            y += self.y_heading
        return reva
        
    def normalize(self):
        """
        Normalize this line so that x_heading is 1, with the exception of
        it being 0, in which case y_heading must be 1.

        Args:
            x (int): X-coordinate of the starting point.
            y (int): Y-coordinate of the starting point.
            x2 (int): X-coordinate of the end point.
            y2 (int): Y-coordinate of the end point.
        """
        if self.x_heading == -1:
            self.x_heading = 1
            self.x -= 4
            if self.y_heading == -1:
                self.y_heading = 1
                self.y -= 4
            elif self.y_heading == 1:
                self.y_heading = -1
                self.y += 4
        elif self.x_heading == 0 and self.y_heading == -1:
            self.y_heading = 1
            self.y -= 4


class Grid:
    """This class models the grid and other elements of the 4+1 solitaire."""

    x_min: int = 0
    x_max: int = 0
    y_min: int = 0
    y_max: int = 0
    focus: list[int, int]

    def __init__(self):
        self.line_count = 0
        self.intersections: dict[tuple[int, int], bool] = {}
        self.line_segments: list[LineSegment] = []
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

    def add_line_to_grid(self, line: Line):
        """
        Add a line to the grid.

        Args:
            line (Line): The line to be added.
        """

        if self.is_valid_line(line):
            for intersection in line.get_intersections():
                self._fill_intersection(intersection.x, intersection.y)
            segments = line.get_segments()
            for segment in segments:
                segment.normalize()
                self._add_line_segment(segment)
            self.line_count += 1

    def _add_line_segment(self, segment: LineSegment):
        """
        Adds a line segment to the grid.

        Args:
            segment (LineSegment): The segment to be added.
        """
        if not isinstance(segment, LineSegment):
            return NotImplemented
        #bisect.insort(self.line_segments, segment)
        self.line_segments.append(segment)
        #self._fill_intersection(segment.x, segment.y)
        #self._fill_intersection(segment.x+segment.x_heading, segment.y+segment.y_heading)

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

    def get_segments(self):
        return self.line_segments
    
    def _has_segment(self, segment: LineSegment) -> bool:
        """
        Checks whether the segment is occupied on the grid.

        Args:
            segment (LineSegment): The segment.

        Returns:
            bool: True if the segment is occupied, False otherwise.
        """
        return segment in self.line_segments

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
    
    def is_valid_line(self, line: Line) -> bool:
        """
        Check if a the given line would be valid to place according to the
        game rules.

        Args:
            line (Line): The proposed line

        Returns:
            True, if the line is valid. False otherwise.
        """
        filled = 0
        empty = 0
        for (x, y) in line.get_intersections():
            if self.is_filled(x, y):
                filled += 1
            else:
                empty +=1
        if filled != 4:
            return False

        for segment in line.get_segments():
            if segment in self.line_segments:
                return False
            
        return True

