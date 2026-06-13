import pytest
from maths.max_sum_sliding_window import max_sum_in_array


def test_max_sum_in_array_normal_case_1():
    arr = [1, 4, 2, 10, 2, 3, 1, 0, 20]
    k = 4
    assert max_sum_in_array(arr, k) == 24


def test_max_sum_in_array_normal_case_2():
    arr = [1, 4, 2, 10, 2, 13, 1, 0, 2]
    k = 4
    assert max_sum_in_array(arr, k) == 27


def test_max_sum_in_array_normal_case_3():
    arr = [5, 2, 8, 1, 9, 3]
    k = 3
    assert max_sum_in_array(arr, k) == 18


def test_max_sum_in_array_single_element_window():
    arr = [1, 4, 2, 10, 2, 3, 1, 0, 20]
    k = 1
    assert max_sum_in_array(arr, k) == 20


def test_max_sum_in_array_entire_array():
    arr = [1, 2, 3, 4, 5]
    k = 5
    assert max_sum_in_array(arr, k) == 15


def test_max_sum_in_array_two_elements():
    arr = [10, 20]
    k = 2
    assert max_sum_in_array(arr, k) == 30


def test_max_sum_in_array_negative_numbers():
    arr = [-1, -2, -3, -4, -5]
    k = 2
    assert max_sum_in_array(arr, k) == -3


def test_max_sum_in_array_mixed_positive_negative():
    arr = [5, -3, 5, -2, 8, 1]
    k = 3
    assert max_sum_in_array(arr, k) == 11


def test_max_sum_in_array_all_zeros():
    arr = [0, 0, 0, 0, 0]
    k = 3
    assert max_sum_in_array(arr, k) == 0


def test_max_sum_in_array_k_greater_than_array_length():
    arr = [1, 4, 2, 10, 2, 3, 1, 0, 20]
    k = 10
    with pytest.raises(ValueError, match="Invalid Input"):
        max_sum_in_array(arr, k)


def test_max_sum_in_array_k_equals_array_length_plus_one():
    arr = [1, 2, 3]
    k = 4
    with pytest.raises(ValueError, match="Invalid Input"):
        max_sum_in_array(arr, k)


def test_max_sum_in_array_negative_k():
    arr = [1, 4, 2, 10, 2, 3, 1, 0, 20]
    k = -1
    with pytest.raises(ValueError, match="Invalid Input"):
        max_sum_in_array(arr, k)


def test_max_sum_in_array_k_zero():
    arr = [1, 4, 2, 10]
    k = 0
    with pytest.raises(ValueError, match="Invalid Input"):
        max_sum_in_array(arr, k)


def test_max_sum_in_array_empty_array():
    arr = []
    k = 1
    with pytest.raises(ValueError, match="Invalid Input"):
        max_sum_in_array(arr, k)


def test_max_sum_in_array_large_numbers():
    arr = [1000, 2000, 3000, 4000, 5000]
    k = 3
    assert max_sum_in_array(arr, k) == 12000