from typing import List
import pytest

import grid

def check_intersection_amount_against(gridi: grid.Grid, target: int, failure_message: str):
    intersection_count: int = 0
    for intsy in gridi.intersections:
        if gridi.is_filled(intsy):
            intersection_count += 1

    assert intersection_count == target, failure_message


def test_adding_and_retrieving_lines():
    gridi: grid.Grid = grid.Grid()

    check_intersection_amount_against(gridi, 36, "Incorrect amount of intersections upon initialization.")

    in_lines: List(grid.Line) = []
    in_lines.append(grid.Line(grid.Intersection(2, 3), 1, 0))
    in_lines.append(grid.Line(grid.Intersection(2, 3), 0, -1))
    in_lines.append(grid.Line(grid.Intersection(-4, 5), 1, 1))
    out_lines: List(grid.Line) = []
    out_lines.append(grid.Line(grid.Intersection(-2, 3), 1, 1))
    out_lines.append(grid.Line(grid.Intersection(2, 3), -1, 0))

    counter: int = 36
    print(f"Starting with: {str(gridi.intersections)}")
    for line in in_lines:
        gridi.add_line_to_grid(line)
        counter += 1
        check_intersection_amount_against(gridi, counter, f"Wrong amount of interactions added upon adding a line. {str(gridi.intersections)}")
    
    intersection_count: int = 0
    for intsy in gridi.intersections:
        if gridi.is_filled(intsy):
            intersection_count += 1

    check_intersection_amount_against(gridi, 39, "Incorrect amount of intersections are populated.")

def test_is_valid_line():
    gridi: grid.Grid = grid.Grid()

    validline   = grid.Line(grid.Intersection(-1, 9), 1, 0)
    invalidline = grid.Line(grid.Intersection(0, 9), 1, 0)

    assert gridi.is_valid_line(validline) == True
    assert gridi.is_valid_line(invalidline) == False

    insects = validline.get_intersections()
    assert grid.Intersection(-1, 9) in insects, "Line has mutated."
    assert grid.Intersection(0, 9) in insects, "Line has mutated."
    assert grid.Intersection(1, 9) in insects, "Line has mutated."
    assert grid.Intersection(2, 9) in insects, "Line has mutated."
    assert grid.Intersection(3, 9) in insects, "Line has mutated."

def test__fill_intersection():
    gridi: grid.Grid = grid.Grid()

    assert len(gridi.intersections) == 36

    sect1 = grid.Intersection(1, 2)
    sect2 = grid.Intersection(2, 2)
    sect3 = grid.Intersection(1, 2)

    gridi._fill_intersection(sect1)
    assert len(gridi.intersections) == 37

    gridi._fill_intersection(sect2)
    assert len(gridi.intersections) == 37

    gridi._fill_intersection(sect3)
    assert len(gridi.intersections) == 37


