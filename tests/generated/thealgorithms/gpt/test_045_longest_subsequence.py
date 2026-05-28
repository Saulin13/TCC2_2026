import pytest
from dynamic_programming.longest_increasing_subsequence import longest_subsequence

def test_longest_subsequence_normal_case():
    assert longest_subsequence([10, 22, 9, 33, 21, 50, 41, 60, 80]) == [10, 22, 33, 41, 60, 80]
    assert longest_subsequence([4, 8, 7, 5, 1, 12, 2, 3, 9]) == [1, 2, 3, 9]
    assert longest_subsequence([28, 26, 12, 23, 35, 39]) == [12, 23, 35, 39]

def test_longest_subsequence_edge_case():
    assert longest_subsequence([9, 8, 7, 6, 5, 7]) == [5, 7]
    assert longest_subsequence([1, 1, 1]) == [1, 1, 1]
    assert longest_subsequence([]) == []
    assert longest_subsequence([1]) == [1]
    assert longest_subsequence([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]
    assert longest_subsequence([5, 4, 3, 2, 1]) == [1]

def test_longest_subsequence_failure_case():
    with pytest.raises(TypeError):
        longest_subsequence(None)
    with pytest.raises(TypeError):
        longest_subsequence("string")
    with pytest.raises(TypeError):
        longest_subsequence(123)