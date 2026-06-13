import pytest
from sorts.recursive_quick_sort import quick_sort

def test_quick_sort_normal_cases():
    assert quick_sort([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]) == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]
    assert quick_sort([10, 7, 8, 9, 1, 5]) == [1, 5, 7, 8, 9, 10]
    assert quick_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]
    assert quick_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

def test_quick_sort_edge_cases():
    assert quick_sort([]) == []
    assert quick_sort([1]) == [1]
    assert quick_sort([2, 1]) == [1, 2]
    assert quick_sort([1, 2, 2, 1]) == [1, 1, 2, 2]
    assert quick_sort([1.1, 2.2, 0.0]) == [0.0, 1.1, 2.2]

def test_quick_sort_failure_cases():
    with pytest.raises(TypeError):
        quick_sort(None)
    with pytest.raises(TypeError):
        quick_sort(123)
    with pytest.raises(TypeError):
        quick_sort([3, 'a', 2])