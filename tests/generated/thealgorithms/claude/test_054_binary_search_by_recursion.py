import pytest
from searches.binary_search import binary_search_by_recursion


def test_find_first_element():
    assert binary_search_by_recursion([0, 5, 7, 10, 15], 0, 0, 4) == 0


def test_find_last_element():
    assert binary_search_by_recursion([0, 5, 7, 10, 15], 15, 0, 4) == 4


def test_find_middle_element():
    assert binary_search_by_recursion([0, 5, 7, 10, 15], 5, 0, 4) == 1


def test_find_element_not_present():
    assert binary_search_by_recursion([0, 5, 7, 10, 15], 6, 0, 4) == -1


def test_find_element_less_than_min():
    assert binary_search_by_recursion([0, 5, 7, 10, 15], -1, 0, 4) == -1


def test_find_element_greater_than_max():
    assert binary_search_by_recursion([0, 5, 7, 10, 15], 20, 0, 4) == -1


def test_single_element_found():
    assert binary_search_by_recursion([5], 5, 0, 0) == 0


def test_single_element_not_found():
    assert binary_search_by_recursion([5], 3, 0, 0) == -1


def test_two_elements_find_first():
    assert binary_search_by_recursion([3, 7], 3, 0, 1) == 0


def test_two_elements_find_second():
    assert binary_search_by_recursion([3, 7], 7, 0, 1) == 1


def test_two_elements_not_found():
    assert binary_search_by_recursion([3, 7], 5, 0, 1) == -1


def test_default_right_parameter():
    assert binary_search_by_recursion([1, 2, 3, 4, 5], 3) == 2


def test_default_right_parameter_not_found():
    assert binary_search_by_recursion([1, 2, 3, 4, 5], 10) == -1


def test_large_list():
    large_list = list(range(0, 1000, 2))
    assert binary_search_by_recursion(large_list, 500) == 250


def test_large_list_not_found():
    large_list = list(range(0, 1000, 2))
    assert binary_search_by_recursion(large_list, 501) == -1


def test_negative_numbers():
    assert binary_search_by_recursion([-10, -5, 0, 5, 10], -5, 0, 4) == 1


def test_all_same_elements_found():
    assert binary_search_by_recursion([5, 5, 5, 5, 5], 5, 0, 4) in [0, 1, 2, 3, 4]


def test_all_same_elements_not_found():
    assert binary_search_by_recursion([5, 5, 5, 5, 5], 3, 0, 4) == -1


def test_unsorted_list_raises_exception():
    with pytest.raises(ValueError, match="sorted_collection must be sorted in ascending order"):
        binary_search_by_recursion([5, 2, 7, 1, 9], 5, 0, 4)


def test_reverse_sorted_list_raises_exception():
    with pytest.raises(ValueError, match="sorted_collection must be sorted in ascending order"):
        binary_search_by_recursion([10, 8, 6, 4, 2], 6, 0, 4)


def test_empty_list():
    assert binary_search_by_recursion([], 5, 0, -1) == -1


def test_find_zero_in_mixed_numbers():
    assert binary_search_by_recursion([-5, -2, 0, 3, 7], 0, 0, 4) == 2


def test_duplicates_find_any_occurrence():
    result = binary_search_by_recursion([1, 2, 3, 3, 3, 4, 5], 3, 0, 6)
    assert result in [2, 3, 4]