import pytest
from other.majority_vote_algorithm import majority_vote

def test_majority_vote_normal_case():
    assert majority_vote([1, 2, 2, 3, 1, 3, 2], 3) == [2]
    assert majority_vote([1, 2, 2, 3, 1, 3, 2], 4) == [1, 2, 3]

def test_majority_vote_no_majority():
    assert majority_vote([1, 2, 2, 3, 1, 3, 2], 2) == []

def test_majority_vote_all_same():
    assert majority_vote([1, 1, 1, 1, 1], 1) == [1]
    assert majority_vote([2, 2, 2, 2, 2], 3) == [2]

def test_majority_vote_empty_votes():
    assert majority_vote([], 1) == []

def test_majority_vote_votes_needed_to_win_greater_than_votes():
    assert majority_vote([1, 2, 3], 5) == []

def test_majority_vote_single_vote():
    assert majority_vote([1], 1) == [1]
    assert majority_vote([1], 2) == []

def test_majority_vote_invalid_votes_needed_to_win():
    with pytest.raises(ZeroDivisionError):
        majority_vote([1, 2, 3], 0)