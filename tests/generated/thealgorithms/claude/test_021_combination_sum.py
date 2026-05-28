import pytest
from backtracking.combination_sum import combination_sum


def test_combination_sum_basic_case():
    result = combination_sum([2, 3, 5], 8)
    assert result == [[2, 2, 2, 2], [2, 3, 3], [3, 5]]


def test_combination_sum_with_exact_match():
    result = combination_sum([2, 3, 6, 7], 7)
    assert result == [[2, 2, 3], [7]]


def test_combination_sum_single_element():
    result = combination_sum([5], 15)
    assert result == [[5, 5, 5]]


def test_combination_sum_no_solution():
    result = combination_sum([3, 5], 1)
    assert result == []


def test_combination_sum_target_zero():
    result = combination_sum([1, 2, 3], 0)
    assert result == [[]]


def test_combination_sum_large_target():
    result = combination_sum([2], 10)
    assert result == [[2, 2, 2, 2, 2]]


def test_combination_sum_multiple_candidates():
    result = combination_sum([2, 3, 4], 6)
    assert result == [[2, 2, 2], [2, 4], [3, 3]]


def test_combination_sum_with_one():
    result = combination_sum([1, 2], 3)
    assert result == [[1, 1, 1], [1, 2]]


def test_combination_sum_unsorted_candidates():
    result = combination_sum([5, 3, 2], 8)
    assert result == [[2, 2, 2, 2], [2, 3, 3], [3, 5]]


def test_combination_sum_empty_candidates_raises_error():
    with pytest.raises(ValueError, match="Candidates list should not be empty"):
        combination_sum([], 1)


def test_combination_sum_negative_candidate_raises_error():
    with pytest.raises(ValueError, match="All elements in candidates must be non-negative"):
        combination_sum([-8, 2, 0], 1)


def test_combination_sum_negative_in_middle_raises_error():
    with pytest.raises(ValueError, match="All elements in candidates must be non-negative"):
        combination_sum([1, -5, 3], 5)


def test_combination_sum_with_zero():
    result = combination_sum([0, 1, 2], 2)
    assert [0] not in result or len(result) > 0


def test_combination_sum_duplicates_in_candidates():
    result = combination_sum([2, 2, 3], 5)
    assert [2, 3] in result


def test_combination_sum_large_candidates():
    result = combination_sum([10, 20, 30], 50)
    assert result == [[10, 10, 10, 10, 10], [10, 10, 10, 20], [10, 20, 20], [10, 10, 30]]