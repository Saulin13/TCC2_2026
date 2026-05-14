import sys
import os
sys.path.append(r'C:\Users\diogo\OneDrive\Área de Trabalho\Diogo\PUC\8 Periodo\TCC\TCC2_2026/repos/Python')
from other.majority_vote_algorithm import majority_vote
import os
import sys




import pytest
from collections import Counter

def majority_vote(votes: list[int], votes_needed_to_win: int) -> list[int]:
    majority_candidate_counter: Counter[int] = Counter()
    for vote in votes:
        majority_candidate_counter[vote] += 1
        if len(majority_candidate_counter) == votes_needed_to_win:
            majority_candidate_counter -= Counter(set(majority_candidate_counter))
    majority_candidate_counter = Counter(
        vote for vote in votes if vote in majority_candidate_counter
    )
    return [
        vote
        for vote in majority_candidate_counter
        if majority_candidate_counter[vote] > len(votes) / votes_needed_to_win
    ]

def test_majority_vote():
    assert majority_vote([1, 2, 2, 3, 1, 3, 2], 3) == [2]
    assert majority_vote([1, 2, 2, 3, 1, 3, 2], 2) == []
    assert majority_vote([1, 2, 2, 3, 1, 3, 2], 4) == [1, 2, 3]
    assert majority_vote([], 1) == []
    assert majority_vote([1, 1, 1, 1], 1) == [1]
    assert majority_vote([1, 2, 3, 4, 5], 5) == [1, 2, 3, 4, 5]
    assert majority_vote([1, 2, 2, 3, 3, 3, 4], 3) == [3]
