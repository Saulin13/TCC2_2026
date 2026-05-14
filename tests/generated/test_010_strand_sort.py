import pytest
from sorts.strand_sort import strand_sort

def test_strand_sort_normal_case():
    assert strand_sort([4, 2, 5, 3, 0, 1]) == [0, 1, 2, 3, 4, 5]
    assert strand_sort([4, 2, 5, 3, 0, 1], reverse=True) == [5, 4, 3, 2, 1, 0]

def test_strand_sort_empty_list():
    assert strand_sort([]) == []
    assert strand_sort([], reverse=True) == []

def test_strand_sort_single_element():
    assert strand_sort([1]) == [1]
    assert strand_sort([1], reverse=True) == [1]

def test_strand_sort_sorted_list():
    assert strand_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]
    assert strand_sort([5, 4, 3, 2, 1], reverse=True) == [5, 4, 3, 2, 1]

def test_strand_sort_reverse_sorted_list():
    assert strand_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]
    assert strand_sort([1, 2, 3, 4, 5], reverse=True) == [5, 4, 3, 2, 1]

def test_strand_sort_duplicates():
    assert strand_sort([4, 2, 5, 3, 0, 1, 3, 2]) == [0, 1, 2, 2, 3, 3, 4, 5]
    assert strand_sort([4, 2, 5, 3, 0, 1, 3, 2], reverse=True) == [5, 4, 3, 3, 2, 2, 1, 0]

def test_strand_sort_all_same_elements():
    assert strand_sort([1, 1, 1, 1]) == [1, 1, 1, 1]
    assert strand_sort([1, 1, 1, 1], reverse=True) == [1, 1, 1, 1]

def test_strand_sort_invalid_input():
    with pytest.raises(TypeError):
        strand_sort(None)
    with pytest.raises(TypeError):
        strand_sort("not a list")