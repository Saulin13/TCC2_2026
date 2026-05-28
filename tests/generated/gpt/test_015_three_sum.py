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

def test_three_sum_single_triplet():
    assert three_sum([-2, 0, 2]) == [[-2, 0, 2]]

def test_three_sum_empty_list():
    assert three_sum([]) == []

def test_three_sum_insufficient_elements():
    assert three_sum([1, 2]) == []
    assert three_sum([1]) == []
    assert three_sum([]) == []

def test_three_sum_duplicates():
    assert three_sum([-1, -1, 2, 2, 0, 0, 1, 1]) == [[-1, -1, 2], [-1, 0, 1]]

def test_three_sum_large_numbers():
    assert three_sum([-1000000, 500000, 500000]) == [[-1000000, 500000, 500000]]

def test_three_sum_exception_path():
    with pytest.raises(TypeError):
        three_sum(None)