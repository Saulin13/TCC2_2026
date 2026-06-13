import pytest
from data_structures.stacks.next_greater_element import next_greatest_element

def test_next_greatest_element_normal_case():
    arr = [4, 5, 2, 25]
    expected = [5, 25, 25, -1]
    assert next_greatest_element(arr) == expected

def test_next_greatest_element_all_decreasing():
    arr = [10, 9, 8, 7]
    expected = [-1, -1, -1, -1]
    assert next_greatest_element(arr) == expected

def test_next_greatest_element_all_increasing():
    arr = [1, 2, 3, 4]
    expected = [2, 3, 4, -1]
    assert next_greatest_element(arr) == expected

def test_next_greatest_element_with_duplicates():
    arr = [4, 5, 2, 5, 3]
    expected = [5, -1, 5, -1, -1]
    assert next_greatest_element(arr) == expected

def test_next_greatest_element_single_element():
    arr = [42]
    expected = [-1]
    assert next_greatest_element(arr) == expected

def test_next_greatest_element_empty_array():
    arr = []
    expected = []
    assert next_greatest_element(arr) == expected

def test_next_greatest_element_large_numbers():
    arr = [1000000, 999999, 1000001]
    expected = [1000001, 1000001, -1]
    assert next_greatest_element(arr) == expected

def test_next_greatest_element_negative_numbers():
    arr = [-1, -2, -3, -4]
    expected = [-1, -1, -1, -1]
    assert next_greatest_element(arr) == expected

def test_next_greatest_element_mixed_numbers():
    arr = [3, -2, 7, 1, 0, 5]
    expected = [7, 7, -1, 5, 5, -1]
    assert next_greatest_element(arr) == expected