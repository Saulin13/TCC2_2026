import pytest
from dynamic_programming.max_non_adjacent_sum import maximum_non_adjacent_sum

def test_maximum_non_adjacent_sum_normal_cases():
    assert maximum_non_adjacent_sum([1, 2, 3]) == 4
    assert maximum_non_adjacent_sum([1, 5, 3, 7, 2, 2, 6]) == 18
    assert maximum_non_adjacent_sum([2, 1, 4, 9, 3, 5]) == 15
    assert maximum_non_adjacent_sum([3, 2, 5, 10, 7]) == 15

def test_maximum_non_adjacent_sum_edge_cases():
    assert maximum_non_adjacent_sum([]) == 0
    assert maximum_non_adjacent_sum([5]) == 5
    assert maximum_non_adjacent_sum([-1, -5, -3, -7, -2, -2, -6]) == 0
    assert maximum_non_adjacent_sum([499, 500, -3, -7, -2, -2, -6]) == 500
    assert maximum_non_adjacent_sum([0, 0, 0, 0]) == 0

def test_maximum_non_adjacent_sum_failure_cases():
    assert maximum_non_adjacent_sum([-1, -2, -3, -4]) == 0
    assert maximum_non_adjacent_sum([-10, 5, -3, 4, -2, 1]) == 9
    assert maximum_non_adjacent_sum([1, -1, 1, -1, 1, -1, 1]) == 3