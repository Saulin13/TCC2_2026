import pytest
from divide_and_conquer.kth_order_statistic import kth_number


def test_kth_number_middle_element():
    assert kth_number([2, 1, 3, 4, 5], 3) == 3


def test_kth_number_first_element():
    assert kth_number([2, 1, 3, 4, 5], 1) == 1


def test_kth_number_last_element():
    assert kth_number([2, 1, 3, 4, 5], 5) == 5


def test_kth_number_second_element():
    assert kth_number([3, 2, 5, 6, 7, 8], 2) == 3


def test_kth_number_fourth_element():
    assert kth_number([25, 21, 98, 100, 76, 22, 43, 60, 89, 87], 4) == 43


def test_kth_number_single_element():
    assert kth_number([42], 1) == 42


def test_kth_number_two_elements_first():
    assert kth_number([5, 3], 1) == 3


def test_kth_number_two_elements_second():
    assert kth_number([5, 3], 2) == 5


def test_kth_number_duplicates():
    assert kth_number([3, 1, 2, 3, 4], 3) == 3


def test_kth_number_all_same():
    assert kth_number([5, 5, 5, 5], 2) == 5


def test_kth_number_negative_numbers():
    assert kth_number([-5, -1, -3, -2, -4], 3) == -3


def test_kth_number_mixed_positive_negative():
    assert kth_number([-2, 5, -1, 3, 0], 2) == -1


def test_kth_number_large_list():
    lst = list(range(100, 0, -1))
    assert kth_number(lst, 50) == 50


def test_kth_number_unsorted_list():
    assert kth_number([9, 3, 7, 1, 5], 4) == 7


def test_kth_number_already_sorted():
    assert kth_number([1, 2, 3, 4, 5], 3) == 3


def test_kth_number_reverse_sorted():
    assert kth_number([5, 4, 3, 2, 1], 3) == 3


def test_kth_number_with_zero():
    assert kth_number([0, -1, 1, -2, 2], 3) == 0


def test_kth_number_empty_list_raises_error():
    with pytest.raises((IndexError, RecursionError, ValueError)):
        kth_number([], 1)


def test_kth_number_k_too_large_raises_error():
    with pytest.raises((IndexError, RecursionError, ValueError)):
        kth_number([1, 2, 3], 5)


def test_kth_number_k_zero_raises_error():
    with pytest.raises((IndexError, RecursionError, ValueError)):
        kth_number([1, 2, 3], 0)


def test_kth_number_k_negative_raises_error():
    with pytest.raises((IndexError, RecursionError, ValueError)):
        kth_number([1, 2, 3], -1)
```