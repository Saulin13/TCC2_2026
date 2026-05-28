import pytest
from searches.binary_search import binary_search_by_recursion

def test_binary_search_found_at_start():
    assert binary_search_by_recursion([0, 5, 7, 10, 15], 0, 0, 4) == 0

def test_binary_search_found_at_end():
    assert binary_search_by_recursion([0, 5, 7, 10, 15], 15, 0, 4) == 4

def test_binary_search_found_in_middle():
    assert binary_search_by_recursion([0, 5, 7, 10, 15], 7, 0, 4) == 2

def test_binary_search_not_found():
    assert binary_search_by_recursion([0, 5, 7, 10, 15], 6, 0, 4) == -1

def test_binary_search_empty_list():
    assert binary_search_by_recursion([], 1, 0, -1) == -1

def test_binary_search_single_element_found():
    assert binary_search_by_recursion([5], 5, 0, 0) == 0

def test_binary_search_single_element_not_found():
    assert binary_search_by_recursion([5], 3, 0, 0) == -1

def test_binary_search_unsorted_list():
    with pytest.raises(ValueError, match="sorted_collection must be sorted in ascending order"):
        binary_search_by_recursion([10, 5, 7, 0, 15], 7, 0, 4)

def test_binary_search_negative_numbers():
    assert binary_search_by_recursion([-10, -5, 0, 5, 10], -5, 0, 4) == 1

def test_binary_search_all_elements_same():
    assert binary_search_by_recursion([7, 7, 7, 7, 7], 7, 0, 4) == 2

def test_binary_search_large_numbers():
    assert binary_search_by_recursion([1000000, 2000000, 3000000], 2000000, 0, 2) == 1