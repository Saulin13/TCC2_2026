import pytest
from maths.max_sum_sliding_window import max_sum_in_array

def test_max_sum_in_array_normal_case():
    arr = [1, 4, 2, 10, 2, 3, 1, 0, 20]
    k = 4
    assert max_sum_in_array(arr, k) == 24

def test_max_sum_in_array_another_normal_case():
    arr = [1, 4, 2, 10, 2, 13, 1, 0, 2]
    k = 4
    assert max_sum_in_array(arr, k) == 27

def test_max_sum_in_array_single_element():
    arr = [5]
    k = 1
    assert max_sum_in_array(arr, k) == 5

def test_max_sum_in_array_all_elements_same():
    arr = [3, 3, 3, 3, 3]
    k = 3
    assert max_sum_in_array(arr, k) == 9

def test_max_sum_in_array_k_equals_array_length():
    arr = [1, 2, 3, 4, 5]
    k = 5
    assert max_sum_in_array(arr, k) == 15

def test_max_sum_in_array_k_greater_than_array_length():
    arr = [1, 2, 3]
    k = 4
    with pytest.raises(ValueError, match="Invalid Input"):
        max_sum_in_array(arr, k)

def test_max_sum_in_array_k_zero():
    arr = [1, 2, 3, 4, 5]
    k = 0
    with pytest.raises(ValueError, match="Invalid Input"):
        max_sum_in_array(arr, k)

def test_max_sum_in_array_empty_array():
    arr = []
    k = 1
    with pytest.raises(ValueError, match="Invalid Input"):
        max_sum_in_array(arr, k)