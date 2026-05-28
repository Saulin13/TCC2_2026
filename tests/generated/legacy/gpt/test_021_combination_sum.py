import pytest
from backtracking.combination_sum import combination_sum

def test_combination_sum_normal_cases():
    assert combination_sum([2, 3, 5], 8) == [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
    assert combination_sum([2, 3, 6, 7], 7) == [[2, 2, 3], [7]]
    assert combination_sum([2, 3, 5], 0) == [[]]

def test_combination_sum_edge_cases():
    assert combination_sum([1], 1) == [[1]]
    assert combination_sum([1], 2) == [[1, 1]]
    assert combination_sum([1, 2], 4) == [[1, 1, 1, 1], [1, 1, 2], [2, 2]]

def test_combination_sum_empty_candidates():
    with pytest.raises(ValueError, match="Candidates list should not be empty"):
        combination_sum([], 1)

def test_combination_sum_negative_candidates():
    with pytest.raises(ValueError, match="All elements in candidates must be non-negative"):
        combination_sum([-8, 2.3, 0], 1)

def test_combination_sum_no_solution():
    assert combination_sum([5, 10], 3) == []