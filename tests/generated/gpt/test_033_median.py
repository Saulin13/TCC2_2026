import pytest
from maths.average_median import median

def test_median_single_element():
    assert median([0]) == 0
    assert median([5]) == 5

def test_median_odd_number_of_elements():
    assert median([3, 1, 2]) == 2
    assert median([7, 5, 3, 1, 9]) == 5

def test_median_even_number_of_elements():
    assert median([4, 1, 3, 2]) == 2.5
    assert median([10, 20, 30, 40]) == 25

def test_median_sorted_list():
    assert median([1, 2, 3, 4, 5]) == 3
    assert median([10, 20, 30, 40, 50, 60]) == 35

def test_median_reverse_sorted_list():
    assert median([5, 4, 3, 2, 1]) == 3
    assert median([60, 50, 40, 30, 20, 10]) == 35

def test_median_with_negative_numbers():
    assert median([-5, -1, -3, -2, -4]) == -3
    assert median([-10, -20, -30, -40]) == -25

def test_median_with_mixed_numbers():
    assert median([-1, 0, 1]) == 0
    assert median([-10, 0, 10, 20]) == 5

def test_median_empty_list():
    with pytest.raises(IndexError):
        median([])

def test_median_large_numbers():
    assert median([1000000000, 2000000000, 3000000000]) == 2000000000
    assert median([1000000000, 2000000000, 3000000000, 4000000000]) == 2500000000