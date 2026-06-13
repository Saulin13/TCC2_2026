import pytest
from bit_manipulation.missing_number import find_missing_number


def test_find_missing_number_basic_case():
    assert find_missing_number([0, 1, 3, 4]) == 2


def test_find_missing_number_unordered():
    assert find_missing_number([4, 3, 1, 0]) == 2


def test_find_missing_number_negative_numbers():
    assert find_missing_number([-4, -3, -1, 0]) == -2


def test_find_missing_number_mixed_negative_positive():
    assert find_missing_number([-2, 2, 1, 3, 0]) == -1


def test_find_missing_number_positive_range():
    assert find_missing_number([1, 3, 4, 5, 6]) == 2


def test_find_missing_number_reverse_order():
    assert find_missing_number([6, 5, 4, 2, 1]) == 3


def test_find_missing_number_random_order():
    assert find_missing_number([6, 1, 5, 3, 4]) == 2


def test_find_missing_number_two_elements():
    assert find_missing_number([0, 2]) == 1


def test_find_missing_number_missing_first():
    assert find_missing_number([1, 2, 3, 4]) == 0


def test_find_missing_number_missing_last():
    assert find_missing_number([0, 1, 2, 3]) == 4


def test_find_missing_number_large_range():
    nums = list(range(0, 100)) + list(range(101, 201))
    assert find_missing_number(nums) == 100


def test_find_missing_number_negative_range():
    assert find_missing_number([-5, -4, -3, -1]) == -2


def test_find_missing_number_single_gap():
    assert find_missing_number([10, 12]) == 11


def test_find_missing_number_empty_list():
    with pytest.raises(ValueError):
        find_missing_number([])


def test_find_missing_number_single_element():
    assert find_missing_number([5]) == 6