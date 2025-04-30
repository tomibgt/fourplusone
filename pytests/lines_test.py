import pytest

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


