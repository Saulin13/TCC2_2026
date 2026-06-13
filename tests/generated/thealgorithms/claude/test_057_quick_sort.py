import pytest
from sorts.recursive_quick_sort import quick_sort


def test_quick_sort_empty_list():
    assert quick_sort([]) == []


def test_quick_sort_single_element():
    assert quick_sort([5]) == [5]


def test_quick_sort_two_elements_sorted():
    assert quick_sort([1, 2]) == [1, 2]


def test_quick_sort_two_elements_unsorted():
    assert quick_sort([2, 1]) == [1, 2]


def test_quick_sort_already_sorted():
    assert quick_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]


def test_quick_sort_reverse_sorted():
    assert quick_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]


def test_quick_sort_unsorted_integers():
    assert quick_sort([3, 1, 4, 1, 5, 9, 2, 6]) == [1, 1, 2, 3, 4, 5, 6, 9]


def test_quick_sort_negative_numbers():
    assert quick_sort([-3, -1, -4, -2]) == [-4, -3, -2, -1]


def test_quick_sort_mixed_positive_negative():
    assert quick_sort([3, -1, 4, -2, 0, 5]) == [-2, -1, 0, 3, 4, 5]


def test_quick_sort_duplicates():
    assert quick_sort([3, 3, 1, 1, 2, 2]) == [1, 1, 2, 2, 3, 3]


def test_quick_sort_all_same():
    assert quick_sort([5, 5, 5, 5]) == [5, 5, 5, 5]


def test_quick_sort_floats():
    assert quick_sort([2.2, 1.1, 3.3, 0.5]) == [0.5, 1.1, 2.2, 3.3]


def test_quick_sort_mixed_int_float():
    assert quick_sort([2, 1.5, 3, 0.5]) == [0.5, 1.5, 2, 3]


def test_quick_sort_string_characters():
    result = quick_sort(list("quick_sort"))
    expected = sorted(list("quick_sort"))
    assert result == expected


def test_quick_sort_strings():
    assert quick_sort(["dog", "cat", "bird", "ant"]) == ["ant", "bird", "cat", "dog"]


def test_quick_sort_large_list():
    data = [9, 7, 5, 3, 1, 2, 4, 6, 8, 0]
    assert quick_sort(data) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_quick_sort_zero_and_positives():
    assert quick_sort([0, 3, 1, 2]) == [0, 1, 2, 3]


def test_quick_sort_zero_and_negatives():
    assert quick_sort([0, -3, -1, -2]) == [-3, -2, -1, 0]