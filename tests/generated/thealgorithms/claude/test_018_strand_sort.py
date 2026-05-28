import pytest
from sorts.strand_sort import strand_sort


def test_strand_sort_empty_list():
    assert strand_sort([]) == []


def test_strand_sort_single_element():
    assert strand_sort([5]) == [5]


def test_strand_sort_two_elements_ordered():
    assert strand_sort([1, 2]) == [1, 2]


def test_strand_sort_two_elements_unordered():
    assert strand_sort([2, 1]) == [1, 2]


def test_strand_sort_basic_ascending():
    assert strand_sort([4, 2, 5, 3, 0, 1]) == [0, 1, 2, 3, 4, 5]


def test_strand_sort_basic_descending():
    assert strand_sort([4, 2, 5, 3, 0, 1], reverse=True) == [5, 4, 3, 2, 1, 0]


def test_strand_sort_already_sorted_ascending():
    assert strand_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]


def test_strand_sort_already_sorted_descending():
    assert strand_sort([5, 4, 3, 2, 1], reverse=True) == [5, 4, 3, 2, 1]


def test_strand_sort_reverse_sorted_ascending():
    assert strand_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]


def test_strand_sort_reverse_sorted_descending():
    assert strand_sort([1, 2, 3, 4, 5], reverse=True) == [5, 4, 3, 2, 1]


def test_strand_sort_duplicates_ascending():
    assert strand_sort([3, 1, 4, 1, 5, 9, 2, 6, 5]) == [1, 1, 2, 3, 4, 5, 5, 6, 9]


def test_strand_sort_duplicates_descending():
    assert strand_sort([3, 1, 4, 1, 5, 9, 2, 6, 5], reverse=True) == [9, 6, 5, 5, 4, 3, 2, 1, 1]


def test_strand_sort_all_same_elements():
    assert strand_sort([7, 7, 7, 7]) == [7, 7, 7, 7]


def test_strand_sort_negative_numbers():
    assert strand_sort([-5, -1, -3, -2, -4]) == [-5, -4, -3, -2, -1]


def test_strand_sort_mixed_positive_negative():
    assert strand_sort([3, -1, 4, -5, 0, 2]) == [-5, -1, 0, 2, 3, 4]


def test_strand_sort_mixed_positive_negative_descending():
    assert strand_sort([3, -1, 4, -5, 0, 2], reverse=True) == [4, 3, 2, 0, -1, -5]


def test_strand_sort_floats():
    assert strand_sort([3.5, 1.2, 4.8, 2.1]) == [1.2, 2.1, 3.5, 4.8]


def test_strand_sort_large_list():
    input_list = [9, 7, 5, 3, 1, 8, 6, 4, 2, 0]
    expected = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert strand_sort(input_list) == expected


def test_strand_sort_with_solution_parameter():
    result = strand_sort([3, 1, 2], reverse=False, solution=[])
    assert result == [1, 2, 3]


def test_strand_sort_with_presorted_solution():
    result = strand_sort([5, 6], reverse=False, solution=[1, 2, 3, 4])
    assert result == [1, 2, 3, 4, 5, 6]


def test_strand_sort_modifies_input_list():
    input_list = [3, 2, 1]
    strand_sort(input_list)
    assert input_list == []


def test_strand_sort_zero_and_positive():
    assert strand_sort([0, 5, 0, 3, 0, 1]) == [0, 0, 0, 1, 3, 5]