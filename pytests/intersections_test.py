import pytest
import random

from grid import *

@pytest.fixture
def basic_testset_of_fixtures():
    testlist = []
    crosses = []
    whys = []
    for i in range(10):
        x = random.randint(-2, 2)
        y = random.randint(-2, 1)
        testlist.append(Intersection(x, y))
        crosses.append(x)
        whys.append(y)
    testlist.append(Intersection(0, 0))
    crosses.append(0)
    whys.append(0)
    testlist.append(Intersection(4, 2))
    crosses.append(4)
    whys.append(2)
    for i in range(10):
        x = random.randint(-2, 2)
        y = random.randint(-2, 1)
        testlist.append(Intersection(x, y))
        crosses.append(x)
        whys.append(y)
    
    yield {"testlist": testlist, "crosses": crosses, "whys": whys}

def test_equality(basic_testset_of_fixtures):
    testlist = basic_testset_of_fixtures["testlist"]
    crosses  = basic_testset_of_fixtures["crosses"]
    whys     = basic_testset_of_fixtures["whys"]

    base_intersection = Intersection(0, 0)
    
    same = []
    diff = []
    for intersection in testlist:
        if base_intersection == intersection:
            same.append(intersection)
        else:
            diff.append(intersection)

    for samis in same:
        assert samis.x == base_intersection.x, f"{samis} doesn't match x!"
        assert samis.y == base_intersection.y, f"{samis} doesn't match y!"
    
    for eri in diff:
        assert eri.x != base_intersection.x or eri.y != base_intersection.y, f"{eri} matches!"

    for i in range(len(testlist)):
        print(f"{testlist[i]} == {crosses[i]}, {whys[i]} ?")
        assert testlist[i].x == crosses[i], f"{crosses[i]}, {whys[i]} has been changed to {testlist[i]}"
        assert testlist[i].y == whys[i], f"{crosses[i]}, {whys[i]} has been changed to {testlist[i]}"
        print(f"{testlist[i]} == {crosses[i]}, {whys[i]} ok")
        