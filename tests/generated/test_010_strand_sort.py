import pytest
from sorts.strand_sort import strand_sort

def test_strand_sort_normal_case():
    assert strand_sort([4, 2, 5, 3, 0, 1]) == [0, 1, 2, 3, 4, 5]
    assert strand_sort([10, 7, 8, 9, 1, 5]) == [1, 5, 7, 8, 9, 10]

def test_strand_sort_reverse_order():
    assert strand_sort([4, 2, 5, 3, 0, 1], reverse=True) == [5, 4, 3, 2, 1, 0]
    assert strand_sort([10, 7, 8, 9, 1, 5], reverse=True) == [10, 9, 8, 7, 5, 1]

def test_strand_sort_empty_list():
    assert strand_sort([]) == []

def test_strand_sort_single_element():
    assert strand_sort([1]) == [1]

def test_strand_sort_identical_elements():
    assert strand_sort([2, 2, 2, 2]) == [2, 2, 2, 2]

def test_strand_sort_already_sorted():
    assert strand_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]
    assert strand_sort([5, 4, 3, 2, 1], reverse=True) == [5, 4, 3, 2, 1]

def test_strand_sort_failure_case():
    with pytest.raises(TypeError):
        strand_sort(None)