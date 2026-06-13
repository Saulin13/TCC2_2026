import pytest
from maths.three_sum import three_sum

def test_three_sum_normal_case():
    assert three_sum([-1, 0, 1, 2, -1, -4]) == [[-1, -1, 2], [-1, 0, 1]]
    assert three_sum([0, -1, 2, -3, 1]) == [[-3, 1, 2], [-1, 0, 1]]

def test_three_sum_no_triplets():
    assert three_sum([1, 2, 3, 4]) == []
    assert three_sum([0, 1, 2, 3]) == []

def test_three_sum_all_zeros():
    assert three_sum([0, 0, 0, 0]) == [[0, 0, 0]]

def test_three_sum_edge_cases():
    assert three_sum([]) == []
    assert three_sum([0]) == []
    assert three_sum([0, 0]) == []
    assert three_sum([0, 0, 0]) == [[0, 0, 0]]

def test_three_sum_large_numbers():
    assert three_sum([1000000, -1000000, 0, 1, 2, -1, -2]) == [[-1000000, 0, 1000000], [-2, 0, 2], [-1, 0, 1]]

def test_three_sum_duplicates():
    assert three_sum([-1, -1, 2, 2, 0, 0, 0, 1, 1]) == [[-1, -1, 2], [-1, 0, 1], [0, 0, 0]]

def test_three_sum_failure_case():
    with pytest.raises(TypeError):
        three_sum(None)