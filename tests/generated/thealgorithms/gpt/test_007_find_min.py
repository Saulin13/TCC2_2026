import pytest
from dynamic_programming.minimum_partition import find_min

def test_find_min_normal_cases():
    assert find_min([1, 2, 3, 4, 5]) == 1
    assert find_min([5, 5, 5, 5, 5]) == 5
    assert find_min([3]) == 3
    assert find_min([9, 9, 9, 9, 9]) == 9
    assert find_min([1, 5, 10, 3]) == 1
    assert find_min(range(10, 0, -1)) == 1

def test_find_min_edge_cases():
    assert find_min([]) == 0
    assert find_min([0, 0, 0, 0]) == 0
    assert find_min([-1, -5, 5, 1]) == 0
    assert find_min([1, 2, 3, 4]) == 0
    assert find_min([-1, 0, 1]) == 0

def test_find_min_exceptions():
    with pytest.raises(IndexError):
        find_min([-1])
    with pytest.raises(IndexError):
        find_min([0, 0, 0, 1, 2, -4])
    with pytest.raises(IndexError):
        find_min([-1, -5, -10, -3])