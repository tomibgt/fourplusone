from __future__ import annotations
from collections import namedtuple
import bisect

class Intersection:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __lt__(self, other: Intersection):
        if not isinstance(other, Intersection):
            return NotImplemented
        if self.x < other.x:
            return True
        if self.x > other.x:
            return False
        if self.y < other.y:
            return True
        if self.y > other.y:
            return False
        return False

    def __le__(self, other: Intersection):
        if not isinstance(other, Intersection):
            return NotImplemented
        if self.x < other.x:
            return True
        if self.x > other.x:
            return False
        if self.y < other.y:
            return True
        if self.y > other.y:
            return False
        return True

    def __eq__(self, other: Intersection):
        if not isinstance(other, Intersection):
            return NotImplemented
        return self.x==other.x and self.y==other.y

    def __ne__(self, other: Intersection):
        if not isinstance(other, Intersection):
            return NotImplemented
        return self.x != other.x or self.y != other.y

    def __gt__(self, other: Intersection):
        if not isinstance(other, Intersection):
            return NotImplemented
        return not self.__le__(other)

    def __ge__(self, other: Intersection):
        if not isinstance(other, Intersection):
            return NotImplemented
        return not self.__lt__(other)
    
    def __hash__(self: Intersection):
        floatx: float = float(self.x)+0.5
        floaty: float = float(self.y)+0.5
        return int(100*floatx/floaty)
    
    def __str__(self: Intersection):
        return f"({self.x}, {self.y})"

    def __repr__(self: Intersection):
        return f"({self.x}, {self.y})"

    def get_copy(self):
        return(Intersection(self.x, self.y))
    

class LineSegment:

    def __init__(self, intersection: Intersection, x_heading: int, y_heading: int):

        if (x_heading, y_heading) not in {
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        }:
            raise ValueError("x_heading and y_heading must each be -1, 0, or 1")

        self.intersection: Intersection = intersection
        self.x_heading: int = x_heading
        self.y_heading: int = y_heading
        self._normalize()

    def __lt__(self, other):
        if not isinstance(other, LineSegment):
            return NotImplemented
        if self.intersection < other.intersection:
            return True
        if self.intersection > other.intersection:
            return False
        if self.x_heading < other.x_heading:
            return True
        if self.x_heading > other.x_heading:
            return False
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
        return (self.intersection, self.x_heading, self.y_heading) == \
               (other.intersection, other.x_heading, other.y_heading)

    def __ne__(self, other):
        if not isinstance(other, LineSegment):
            return NotImplemented
        return (self.intersection, self.x_heading, self.y_heading) != \
               (other.intersection, other.x_heading, other.y_heading)

    def __gt__(self, other):
        if not isinstance(other, LineSegment):
            return NotImplemented
        return not self.__le__(other)

    def __ge__(self, other):
        if not isinstance(other, LineSegment):
            return NotImplemented
        return not self.__lt__(other)
    
    def __hash__(self):
        return hash((self.intersection.__hash__(), self.x_heading, self.y_heading))
    
    def __str__(self):
        return f"({self.intersection}: {self.x_heading}, {self.y_heading})"

    def __repr__(self):
        return f"({self.intersection}: {self.x_heading}, {self.y_heading})"

    def _normalize(self):
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
            self.intersection.x -= 1
            if self.y_heading == -1:
                self.y_heading = 1
                self.intersection.y -= 1
            elif self.y_heading == 1:
                self.y_heading = -1
                self.intersection.y += 1
        elif self.x_heading == 0 and self.y_heading == -1:
            self.y_heading = 1
            self.intersection.y -= 1

class Line:

    Point = namedtuple('Point', ['x', 'y'])

    def __init__(self, intersection: Intersection, x_heading: int, y_heading: int):
        if (x_heading, y_heading) not in {
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        }:
            raise ValueError("x_heading and y_heading must each be -1, 0, or 1")
        
        self.intersection: Intersection = intersection
        self.x_heading: int = x_heading
        self.y_heading: int = y_heading
        self._normalize()

    def __lt__(self, other):
        if not isinstance(other, Line):
            return NotImplemented
        if self.intersection.x < other.intersection.x:
            return True
        if self.intersection.x > other.intersection.x:
            return False
        if self.intersection.y < other.intersection.y:
            return True
        if self.intersection.y > other.intersection.y:
            return False
        if self.x_heading < other.x_heading:
            return True
        if self.x_heading > other.x_heading:
            return False
        if self.y_heading < other.y_heading:
            return True
        return False


    def __le__(self, other):
        if not isinstance(other, Line):
            return NotImplemented
        if self.__lt__(other) or self.__eq__(other):
            return True
        return False

    def __eq__(self, other):
        if not isinstance(other, Line):
            return NotImplemented
        return (self.intersection, self.x_heading, self.y_heading) == \
               (other.intersection, other.x_heading, other.y_heading)

    def __ne__(self, other):
        if not isinstance(other, Line):
            return NotImplemented
        return (self.intersection, self.x_heading, self.y_heading) != \
               (other.intersection, other.x_heading, other.y_heading)

    def __gt__(self, other):
        if not isinstance(other, Line):
            return NotImplemented
        return not self.__le__(other)

    def __ge__(self, other):
        if not isinstance(other, Line):
            return NotImplemented
        return not self.__lt__(other)
    
    def __hash__(self):
        return hash((self.intersection, self.x_heading, self.y_heading))

    def __str__(self):
        return f"({self.intersection}; {self.x_heading}; {self.y_heading})"

    def __repr__(self):
        return f"({self.intersection}; {self.x_heading}; {self.y_heading})"
    
    def get_intersections(self):
        reva: list[Intersection] = []
        x = self.intersection.x
        y = self.intersection.y
        for i in range(5):
            reva.append(Intersection(x, y))
            x += self.x_heading
            y += self.y_heading
        return reva

    def get_segments(self):
        """
        Returns the line segments that compose this line.

        Returns:
            list[LineSegment]: The list of normalized segments.
        """
        reva: list[LineSegment] = []
        intersection = self.intersection.get_copy()
        for i in range(4):
            segment = LineSegment(intersection, self.x_heading, self.y_heading)
            reva.append(segment)
            intersection.x += self.x_heading
            intersection.y += self.y_heading
        return reva
        
    def _normalize(self):
        """
        Normalize this line so that x_heading is 1, with the exception of
        it being 0, in which case y_heading must be 1.
        """
        if self.x_heading == -1:
            self.x_heading = 1
            self.intersection.x -= 4
            if self.y_heading == -1:
                self.y_heading = 1
                self.intersection.y -= 4
            elif self.y_heading == 1:
                self.y_heading = -1
                self.intersection.y += 4
        elif self.x_heading == 0 and self.y_heading == -1:
            self.y_heading = 1
            self.intersection.y -= 4


class Grid:
    """This class models the grid and other elements of the 4+1 solitaire."""

    x_min: int = 0
    x_max: int = 0
    y_min: int = 0
    y_max: int = 0
    focus: list[int, int]

    def __init__(self):
        self.line_count = 0
        self.intersections: dict[Intersection, bool] = {}
        self.line_segments: list[LineSegment] = []
        """Initialize the grid with the initial plus laid on it."""
        for i in range(3):
            self._fill_intersection(Intersection(  i  ,   0  ))
            self._fill_intersection(Intersection(i - 3,   3  ))
            self._fill_intersection(Intersection(i + 3,   3  ))
            self._fill_intersection(Intersection(i - 4,   6  ))
            self._fill_intersection(Intersection(i + 2,   6  ))
            self._fill_intersection(Intersection(i - 1,   9  ))
            self._fill_intersection(Intersection(  2  , i + 1))
            self._fill_intersection(Intersection( -1  ,   i  ))
            self._fill_intersection(Intersection(  5  , i + 4))
            self._fill_intersection(Intersection(  2  , i + 7))
            self._fill_intersection(Intersection( -1  , i + 6))
            self._fill_intersection(Intersection( -4  , i + 3))

    def add_line_to_grid(self, line: Line):
        """
        Add a line to the grid.

        Args:
            line (Line): The line to be added.
        """

        if self.is_valid_line(line):
            for intersection in line.get_intersections():
                self._fill_intersection(intersection)
            segments = line.get_segments()
            for segment in segments:
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

    def _fill_intersection(self, intersection: Intersection):
        """
        Mark the intersection (x, y) as filled.

        If the intersection is outside the x_min, x_max, y_min, y_max scope,
        extends the scope.

        Args:
            intersection (Intersection): The intersection.
        """
        self.intersections[intersection] = True
        if intersection.x > Grid.x_max:
            Grid.x_max = intersection.x
        if intersection.y > Grid.y_max:
            Grid.y_max = intersection.y
        if intersection.x < Grid.x_min:
            Grid.x_min = intersection.x
        if intersection.y < Grid.y_min:
            Grid.y_min = intersection.y

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

    def is_filled(self, intersection: Intersection) -> bool:
        """
        Checks if the intersection is filled in this grid.

        Args:
            intersection (Intersection): The intersection.

        Returns:
            bool: True, if the intersection is filled, False otherwise.
        """
        if intersection in self.intersections:
            return self.intersections[intersection]
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
        for intersection in line.get_intersections():
            if self.is_filled(intersection):
                filled += 1
            else:
                empty +=1
        if filled != 4:
            return False

        for segment in line.get_segments():
            if segment in self.line_segments:
                return False

        return True

