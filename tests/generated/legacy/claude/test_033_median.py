import pytest
from maths.average_median import median


def test_median_single_element():
    assert median([0]) == 0
    assert median([5]) == 5
    assert median([-3]) == -3


def test_median_odd_length():
    assert median([1, 2, 3]) == 2
    assert median([2, 70, 6, 50, 20, 8, 4]) == 8
    assert median([5, 1, 9]) == 5
    assert median([10, 20, 30, 40, 50]) == 30


def test_median_even_length():
    assert median([4, 1, 3, 2]) == 2.5
    assert median([1, 2]) == 1.5
    assert median([10, 20, 30, 40]) == 25.0
    assert median([5, 15, 25, 35]) == 20.0


def test_median_negative_numbers():
    assert median([-5, -1, -3]) == -3
    assert median([-10, -20, -30, -40]) == -25.0
    assert median([-1, 1]) == 0.0


def test_median_mixed_positive_negative():
    assert median([-5, 0, 5]) == 0
    assert median([-10, -5, 5, 10]) == 0.0
    assert median([-3, -1, 2, 4, 6]) == 2


def test_median_duplicates():
    assert median([5, 5, 5]) == 5
    assert median([1, 1, 2, 2]) == 1.5
    assert median([3, 3, 3, 3, 3]) == 3


def test_median_unsorted_input():
    assert median([9, 1, 5, 3, 7]) == 5
    assert median([100, 10, 50, 30]) == 40.0


def test_median_floats():
    assert median([1.5, 2.5, 3.5]) == 2.5
    assert median([1.1, 2.2, 3.3, 4.4]) == 2.75


def test_median_empty_list():
    with pytest.raises(IndexError):
        median([])


def test_median_two_elements():
    assert median([1, 3]) == 2.0
    assert median([10, 20]) == 15.0