import pytest
from data_structures.stacks.next_greater_element import next_greatest_element


def test_next_greatest_element_basic():
    arr = [4, 5, 2, 10]
    expected = [5, 10, 10, -1]
    assert next_greatest_element(arr) == expected


def test_next_greatest_element_ascending():
    arr = [1, 2, 3, 4, 5]
    expected = [2, 3, 4, 5, -1]
    assert next_greatest_element(arr) == expected


def test_next_greatest_element_descending():
    arr = [5, 4, 3, 2, 1]
    expected = [-1, -1, -1, -1, -1]
    assert next_greatest_element(arr) == expected


def test_next_greatest_element_single_element():
    arr = [42]
    expected = [-1]
    assert next_greatest_element(arr) == expected


def test_next_greatest_element_two_elements_increasing():
    arr = [3, 7]
    expected = [7, -1]
    assert next_greatest_element(arr) == expected


def test_next_greatest_element_two_elements_decreasing():
    arr = [7, 3]
    expected = [-1, -1]
    assert next_greatest_element(arr) == expected


def test_next_greatest_element_with_duplicates():
    arr = [4, 5, 5, 2, 10, 10]
    expected = [5, 10, 10, 10, -1, -1]
    assert next_greatest_element(arr) == expected


def test_next_greatest_element_all_same():
    arr = [3, 3, 3, 3]
    expected = [-1, -1, -1, -1]
    assert next_greatest_element(arr) == expected


def test_next_greatest_element_with_negatives():
    arr = [-5, -2, -8, 0, 3]
    expected = [-2, 0, 0, 3, -1]
    assert next_greatest_element(arr) == expected


def test_next_greatest_element_with_floats():
    arr = [1.5, 2.7, 1.2, 3.9]
    expected = [2.7, 3.9, 3.9, -1]
    assert next_greatest_element(arr) == expected


def test_next_greatest_element_empty_array():
    arr = []
    expected = []
    assert next_greatest_element(arr) == expected


def test_next_greatest_element_mixed_positive_negative():
    arr = [3, -1, 5, -2, 7]
    expected = [5, 5, 7, 7, -1]
    assert next_greatest_element(arr) == expected


def test_next_greatest_element_peak_in_middle():
    arr = [1, 3, 2, 4]
    expected = [3, 4, 4, -1]
    assert next_greatest_element(arr) == expected


def test_next_greatest_element_large_numbers():
    arr = [1000000, 999999, 1000001]
    expected = [1000001, 1000001, -1]
    assert next_greatest_element(arr) == expected


def test_next_greatest_element_zeros():
    arr = [0, 0, 0]
    expected = [-1, -1, -1]
    assert next_greatest_element(arr) == expected


def test_next_greatest_element_alternating():
    arr = [1, 5, 2, 6, 3, 7]
    expected = [5, 6, 6, 7, 7, -1]
    assert next_greatest_element(arr) == expected