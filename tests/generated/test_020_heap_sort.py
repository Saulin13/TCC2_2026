import pytest
from sorts.intro_sort import heap_sort

def test_heap_sort_normal_case():
    assert heap_sort([4, 2, 6, 8, 1, 7, 8, 22, 14, 56, 27, 79, 23, 45, 14, 12]) == [1, 2, 4, 6, 7, 8, 8, 12, 14, 14, 22, 23, 27, 45, 56, 79]
    assert heap_sort([-2, -11, 0, 0, 0, 87, 45, -69, 78, 12, 10, 103, 89, 52]) == [-69, -11, -2, 0, 0, 0, 10, 12, 45, 52, 78, 87, 89, 103]
    assert heap_sort(['b', 'd', 'e', 'f', 'g', 'p', 'x', 'z', 'b', 's', 'e', 'u', 'v']) == ['b', 'b', 'd', 'e', 'e', 'f', 'g', 'p', 's', 'u', 'v', 'x', 'z']
    assert heap_sort([6.2, -45.54, 8465.20, 758.56, -457.0, 0, 1, 2.879, 1.7, 11.7]) == [-457.0, -45.54, 0, 1, 1.7, 2.879, 6.2, 11.7, 758.56, 8465.2]

def test_heap_sort_edge_cases():
    assert heap_sort([]) == []
    assert heap_sort([1]) == [1]
    assert heap_sort([2, 1]) == [1, 2]
    assert heap_sort([1, 1, 1, 1]) == [1, 1, 1, 1]

def test_heap_sort_failure_case():
    with pytest.raises(TypeError):
        heap_sort([1, 'a', 3.5, None])