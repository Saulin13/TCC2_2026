import pytest
from maths.average_median import median

def test_median_single_element():
    assert median([0]) == 0
    assert median([5]) == 5

def test_median_odd_number_of_elements():
    assert median([4, 1, 3, 2, 5]) == 3
    assert median([2, 70, 6, 50, 20, 8, 4]) == 8

def test_median_even_number_of_elements():
    assert median([4, 1, 3, 2]) == 2.5
    assert median([10, 20, 30, 40]) == 25

def test_median_sorted_input():
    assert median([1, 2, 3, 4, 5]) == 3
    assert median([1, 2, 3, 4]) == 2.5

def test_median_reverse_sorted_input():
    assert median([5, 4, 3, 2, 1]) == 3
    assert median([4, 3, 2, 1]) == 2.5

def test_median_with_negative_numbers():
    assert median([-5, -1, -3, -2, -4]) == -3
    assert median([-2, -1, -3, -4]) == -2.5

def test_median_mixed_positive_and_negative_numbers():
    assert median([-1, 0, 1]) == 0
    assert median([-10, 0, 10, 20]) == 5

def test_median_large_numbers():
    assert median([1000000, 500000, 1000001]) == 1000000
    assert median([1000000, 500000, 1000001, 500001]) == 750000.5

def test_median_empty_list():
    with pytest.raises(IndexError):
        median([])

def test_median_non_integer_values():
    assert median([1.5, 2.5, 3.5]) == 2.5
    assert median([1.5, 2.5, 3.5, 4.5]) == 3.0