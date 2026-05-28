import pytest
from sorts.recursive_quick_sort import quick_sort

def test_quick_sort_normal_cases():
    assert quick_sort([3, 1, 2]) == [1, 2, 3]
    assert quick_sort([5, 3, 8, 6, 2]) == [2, 3, 5, 6, 8]
    assert quick_sort([10, 7, 8, 9, 1, 5]) == [1, 5, 7, 8, 9, 10]
    assert quick_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]
    assert quick_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

def test_quick_sort_edge_cases():
    assert quick_sort([]) == []
    assert quick_sort([1]) == [1]
    assert quick_sort([2, 1]) == [1, 2]
    assert quick_sort([1, 1, 1, 1]) == [1, 1, 1, 1]
    assert quick_sort([1, 2, 2, 1]) == [1, 1, 2, 2]

def test_quick_sort_with_strings():
    assert quick_sort(['banana', 'apple', 'cherry']) == ['apple', 'banana', 'cherry']
    assert quick_sort(['a', 'b', 'a']) == ['a', 'a', 'b']

def test_quick_sort_with_floats():
    assert quick_sort([2.2, 1.1, 3.3]) == [1.1, 2.2, 3.3]
    assert quick_sort([1.5, 1.2, 1.3]) == [1.2, 1.3, 1.5]

def test_quick_sort_failure_case():
    with pytest.raises(TypeError):
        quick_sort([1, 'a', 3])