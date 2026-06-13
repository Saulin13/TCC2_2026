import pytest
from searches.binary_search import binary_search_by_recursion


def test_binary_search_find_first_element():
    assert binary_search_by_recursion([0, 5, 7, 10, 15], 0, 0, 4) == 0


def test_binary_search_find_last_element():
    assert binary_search_by_recursion([0, 5, 7, 10, 15], 15, 0, 4) == 4


def test_binary_search_find_middle_element():
    assert binary_search_by_recursion([0, 5, 7, 10, 15], 7, 0, 4) == 2


def test_binary_search_find_element_at_index_1():
    assert binary_search_by_recursion([0, 5, 7, 10, 15], 5, 0, 4) == 1


def test_binary_search_element_not_found():
    assert binary_search_by_recursion([0, 5, 7, 10, 15], 6, 0, 4) == -1


def test_binary_search_element_not_found_too_small():
    assert binary_search_by_recursion([0, 5, 7, 10, 15], -1, 0, 4) == -1


def test_binary_search_element_not_found_too_large():
    assert binary_search_by_recursion([0, 5, 7, 10, 15], 20, 0, 4) == -1


def test_binary_search_single_element_found():
    assert binary_search_by_recursion([5], 5, 0, 0) == 0


def test_binary_search_single_element_not_found():
    assert binary_search_by_recursion([5], 3, 0, 0) == -1


def test_binary_search_two_elements_find_first():
    assert binary_search_by_recursion([3, 7], 3, 0, 1) == 0


def test_binary_search_two_elements_find_second():
    assert binary_search_by_recursion([3, 7], 7, 0, 1) == 1


def test_binary_search_two_elements_not_found():
    assert binary_search_by_recursion([3, 7], 5, 0, 1) == -1


def test_binary_search_with_default_right_parameter():
    assert binary_search_by_recursion([1, 2, 3, 4, 5], 3) == 2


def test_binary_search_with_default_parameters_found():
    assert binary_search_by_recursion([10, 20, 30, 40, 50], 40) == 3


def test_binary_search_with_default_parameters_not_found():
    assert binary_search_by_recursion([10, 20, 30, 40, 50], 25) == -1


def test_binary_search_large_list():
    large_list = list(range(0, 1000, 2))
    assert binary_search_by_recursion(large_list, 500) == 250


def test_binary_search_large_list_not_found():
    large_list = list(range(0, 1000, 2))
    assert binary_search_by_recursion(large_list, 501) == -1


def test_binary_search_negative_numbers():
    assert binary_search_by_recursion([-50, -30, -10, 0, 10, 30], -10) == 2


def test_binary_search_all_negative_numbers():
    assert binary_search_by_recursion([-100, -80, -60, -40, -20], -60) == 2


def test_binary_search_duplicate_values():
    result = binary_search_by_recursion([1, 2, 3, 3, 3, 4, 5], 3)
    assert result in [2, 3, 4]


def test_binary_search_unsorted_list_raises_exception():
    with pytest.raises(ValueError, match="sorted_collection must be sorted in ascending order"):
        binary_search_by_recursion([5, 2, 8, 1, 9], 5, 0, 4)


def test_binary_search_descending_list_raises_exception():
    with pytest.raises(ValueError, match="sorted_collection must be sorted in ascending order"):
        binary_search_by_recursion([10, 8, 6, 4, 2], 6, 0, 4)


def test_binary_search_empty_list():
    assert binary_search_by_recursion([], 5, 0, -1) == -1


def test_binary_search_with_explicit_left_right():
    assert binary_search_by_recursion([1, 3, 5, 7, 9, 11, 13], 9, 2, 6) == 4