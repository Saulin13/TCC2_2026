import pytest
from dynamic_programming.max_non_adjacent_sum import maximum_non_adjacent_sum


def test_simple_case_three_elements():
    assert maximum_non_adjacent_sum([1, 2, 3]) == 4


def test_longer_sequence():
    assert maximum_non_adjacent_sum([1, 5, 3, 7, 2, 2, 6]) == 18


def test_all_negative_numbers():
    assert maximum_non_adjacent_sum([-1, -5, -3, -7, -2, -2, -6]) == 0


def test_mixed_with_large_positive():
    assert maximum_non_adjacent_sum([499, 500, -3, -7, -2, -2, -6]) == 500


def test_empty_list():
    assert maximum_non_adjacent_sum([]) == 0


def test_single_element_positive():
    assert maximum_non_adjacent_sum([5]) == 5


def test_single_element_negative():
    assert maximum_non_adjacent_sum([-5]) == 0


def test_two_elements_both_positive():
    assert maximum_non_adjacent_sum([3, 5]) == 5


def test_two_elements_both_negative():
    assert maximum_non_adjacent_sum([-3, -5]) == 0


def test_two_elements_mixed():
    assert maximum_non_adjacent_sum([3, -5]) == 3


def test_alternating_high_low():
    assert maximum_non_adjacent_sum([5, 1, 5, 1, 5]) == 15


def test_all_same_positive():
    assert maximum_non_adjacent_sum([4, 4, 4, 4]) == 8


def test_all_zeros():
    assert maximum_non_adjacent_sum([0, 0, 0, 0]) == 0


def test_zeros_and_positives():
    assert maximum_non_adjacent_sum([0, 5, 0, 5, 0]) == 10


def test_large_numbers():
    assert maximum_non_adjacent_sum([1000, 2000, 3000]) == 4000


def test_negative_and_positive_mixed():
    assert maximum_non_adjacent_sum([5, -2, 10, -7, 3]) == 18


def test_descending_order():
    assert maximum_non_adjacent_sum([10, 9, 8, 7, 6]) == 24


def test_ascending_order():
    assert maximum_non_adjacent_sum([1, 2, 3, 4, 5]) == 9


def test_type_error_with_none():
    with pytest.raises(TypeError):
        maximum_non_adjacent_sum(None)


def test_type_error_with_string():
    with pytest.raises(TypeError):
        maximum_non_adjacent_sum("not a list")


def test_type_error_with_non_numeric_elements():
    with pytest.raises(TypeError):
        maximum_non_adjacent_sum([1, 2, "three", 4])