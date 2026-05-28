import pytest
from divide_and_conquer.kth_order_statistic import kth_number

def test_kth_number_normal_cases():
    assert kth_number([2, 1, 3, 4, 5], 3) == 3
    assert kth_number([2, 1, 3, 4, 5], 1) == 1
    assert kth_number([2, 1, 3, 4, 5], 5) == 5
    assert kth_number([3, 2, 5, 6, 7, 8], 2) == 3
    assert kth_number([25, 21, 98, 100, 76, 22, 43, 60, 89, 87], 4) == 43

def test_kth_number_edge_cases():
    assert kth_number([1], 1) == 1
    assert kth_number([1, 2], 1) == 1
    assert kth_number([1, 2], 2) == 2
    assert kth_number([2, 1], 1) == 1
    assert kth_number([2, 1], 2) == 2

def test_kth_number_failure_cases():
    with pytest.raises(IndexError):
        kth_number([], 1)
    with pytest.raises(IndexError):
        kth_number([1, 2, 3], 0)
    with pytest.raises(IndexError):
        kth_number([1, 2, 3], 4)