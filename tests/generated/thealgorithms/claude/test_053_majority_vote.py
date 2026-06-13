import pytest
from collections import Counter
from other.majority_vote_algorithm import majority_vote


def test_majority_vote_basic_case():
    result = majority_vote([1, 2, 2, 3, 1, 3, 2], 3)
    assert result == [2]


def test_majority_vote_no_majority():
    result = majority_vote([1, 2, 2, 3, 1, 3, 2], 2)
    assert result == []


def test_majority_vote_multiple_candidates():
    result = majority_vote([1, 2, 2, 3, 1, 3, 2], 4)
    assert sorted(result) == [1, 2, 3]


def test_majority_vote_single_candidate():
    result = majority_vote([5, 5, 5, 5, 5], 2)
    assert result == [5]


def test_majority_vote_all_same():
    result = majority_vote([7, 7, 7, 7], 3)
    assert result == [7]


def test_majority_vote_empty_list():
    result = majority_vote([], 2)
    assert result == []


def test_majority_vote_single_element():
    result = majority_vote([1], 2)
    assert result == [1]


def test_majority_vote_votes_needed_one():
    result = majority_vote([1, 2, 3, 4, 5], 1)
    assert result == []


def test_majority_vote_votes_needed_equals_unique_count():
    result = majority_vote([1, 1, 2, 2, 3, 3], 3)
    assert sorted(result) == [1, 2, 3]


def test_majority_vote_large_votes_needed():
    result = majority_vote([1, 1, 1, 2, 2, 3], 10)
    assert sorted(result) == [1, 2, 3]


def test_majority_vote_two_candidates_one_majority():
    result = majority_vote([1, 1, 1, 2, 2], 2)
    assert result == [1]


def test_majority_vote_exact_threshold():
    result = majority_vote([1, 1, 2, 2, 3, 3], 2)
    assert result == []


def test_majority_vote_just_above_threshold():
    result = majority_vote([1, 1, 1, 2, 2], 3)
    assert result == [1]


def test_majority_vote_negative_numbers():
    result = majority_vote([-1, -1, -1, -2, -2], 2)
    assert result == [-1]


def test_majority_vote_mixed_positive_negative():
    result = majority_vote([-1, -1, -1, 1, 1, 1, 0], 3)
    assert sorted(result) == [-1, 1]


def test_majority_vote_zero_votes_needed():
    with pytest.raises(ZeroDivisionError):
        majority_vote([1, 2, 3], 0)


def test_majority_vote_large_dataset():
    votes = [1] * 100 + [2] * 50 + [3] * 30
    result = majority_vote(votes, 2)
    assert result == [1]


def test_majority_vote_uniform_distribution():
    result = majority_vote([1, 2, 3, 4, 5, 6], 3)
    assert result == []