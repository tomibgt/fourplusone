import pytest
from collections import Counter

import grid

def test_intersections_generation():
    test_line: grid.Line = grid.Line(grid.Intersection(0, 0), 1, -1)
    nulnul: bool = False
    oneone: bool = False
    twotwo: bool = False
    thrthr: bool = False
    forfor: bool = False
    for insect in test_line.get_intersections():
        if insect.x == 0 and insect.y == 0:
            nulnul = True
        elif insect.x == 1 and insect.y == -1:
            oneone = True
        elif insect.x == 2 and insect.y == -2:
            twotwo = True
        elif insect.x == 3 and insect.y == -3:
            thrthr = True
        elif insect.x == 4 and insect.y == -4:
            forfor = True
        else:
            assert False, f"This intersection doesn't belong: {insect}"
    insects: list[grid.Intersection] = test_line.get_intersections()
    assert grid.Intersection(0,0) in insects, "Line has mutated."
    assert grid.Intersection(1,-1) in insects, "Line has mutated."
    assert grid.Intersection(2,-2) in insects, "Line has mutated."
    assert grid.Intersection(3,-3) in insects, "Line has mutated."
    assert grid.Intersection(4,-4) in insects, "Line has mutated."
    
    assert nulnul == True and oneone == True and twotwo == True and thrthr == True and forfor == True

    headings: list[tuple[int, int]]= [(1,1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0)]
    for heading in headings:
        line: grid.Line = grid.Line(grid.Intersection(0, 0), heading[0], heading[1])
        checklist: list[bool] = [False, False, False, False, False]
        insect_count: int = 0
        for insect in line.get_intersections():
            cursor: list[int, int] = [0, 0]
            for i in range(5):
                if insect.x == cursor[0] and insect.y == cursor[1]:
                    checklist[i] = True
                cursor[0] += heading[0]
                cursor[1] += heading[1]
            insect_count += 1
            assert insect_count < 6, "Too many intersections."
        for checklistcheck in checklist:
            assert checklistcheck, f"A correct intersection is missing from {heading}:{checklist} / {line.get_intersections()}."

def test_normalize():
    # An instantiated line should always first normalize itself.
    i11 = grid.Intersection(1, 1)
    i15 = grid.Intersection(1, 5)
    i19 = grid.Intersection(1, 9)
    i22 = grid.Intersection(2, 2)
    i25 = grid.Intersection(2, 5)
    i28 = grid.Intersection(2, 8)
    i33 = grid.Intersection(3, 3)
    i35 = grid.Intersection(3, 5)
    i37 = grid.Intersection(3, 7)
    i44 = grid.Intersection(4, 4)
    i45 = grid.Intersection(4, 5)
    i46 = grid.Intersection(4, 6)
    i51 = grid.Intersection(5, 1)
    i52 = grid.Intersection(5, 2)
    i53 = grid.Intersection(5, 3)
    i54 = grid.Intersection(5, 4)
    i55 = grid.Intersection(5, 5)
    i56 = grid.Intersection(5, 6)
    i57 = grid.Intersection(5, 7)
    i58 = grid.Intersection(5, 8)
    i59 = grid.Intersection(5, 9)
    i64 = grid.Intersection(6, 4)
    i65 = grid.Intersection(6, 5)
    i66 = grid.Intersection(6, 6)
    i73 = grid.Intersection(7, 3)
    i75 = grid.Intersection(7, 5)
    i77 = grid.Intersection(7, 7)
    i82 = grid.Intersection(8, 2)
    i85 = grid.Intersection(8, 5)
    i88 = grid.Intersection(8, 8)
    i91 = grid.Intersection(9, 1)
    i95 = grid.Intersection(9, 5)
    i99 = grid.Intersection(9, 9)
    test_line = grid.Line(i55, 1, -1)
    assert Counter(test_line.get_intersections()) == Counter([i55, i64, i73, i82, i91]), "1,-1 heading doesn't need normalizing."
    assert test_line.intersection == i55
    test_line = grid.Line(i55, 1, 0)
    assert Counter(test_line.get_intersections()) == Counter([i55, i65, i75, i85, i95]), "1,0 heading doesn't need normalizing."
    assert test_line.intersection == i55
    test_line = grid.Line(i55, 1, 1)
    assert Counter(test_line.get_intersections()) == Counter([i55, i66, i77, i88, i99]), "1,1 heading doesn't need normalizing."
    test_line = grid.Line(i55, 0, 1)
    assert test_line.intersection == i55
    assert Counter(test_line.get_intersections()) == Counter([i55, i56, i57, i58, i59]), "0,1 heading doesn't need normalizing."
    test_line = grid.Line(i55, -1, 1)
    assert Counter(test_line.get_intersections()) == Counter([i55, i46, i37, i28, i19]), f"-1,1 intersections moved: {[i55, i46, i37, i28, i19]} -> {test_line.get_intersections()}"
    assert test_line.intersection == i19
    test_line = grid.Line(i55, -1, 0)
    assert Counter(test_line.get_intersections()) == Counter([i55, i45, i35, i25, i15]), f"-1,0 intersections moved: {[i55, i45, i35, i25, i15]} -> {test_line.get_intersections()}"
    assert test_line.intersection == i15
    test_line = grid.Line(i55, -1, -1)
    assert Counter(test_line.get_intersections()) == Counter([i55, i44, i33, i22, i11]), f"-1,-1 intersections moved: {[i55, i44, i33, i22, i11]} -> {test_line.get_intersections()}"
    assert test_line.intersection == i11
    test_line = grid.Line(i55, 0, -1)
    assert Counter(test_line.get_intersections()) == Counter([i55, i54, i53, i52, i51]), f"0,-1 intersections moved: {[i55, i54, i53, i52, i51]} -> {test_line.get_intersections()}"
    assert test_line.intersection == i51

