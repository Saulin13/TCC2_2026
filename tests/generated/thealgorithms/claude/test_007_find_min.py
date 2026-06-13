import pytest
from dynamic_programming.minimum_partition import find_min


def test_find_min_normal_case_odd_sum():
    assert find_min([1, 2, 3, 4, 5]) == 1


def test_find_min_all_same_odd_count():
    assert find_min([5, 5, 5, 5, 5]) == 5


def test_find_min_all_same_even_count():
    assert find_min([5, 5, 5, 5]) == 0


def test_find_min_single_element():
    assert find_min([3]) == 3


def test_find_min_empty_list():
    assert find_min([]) == 0


def test_find_min_even_partition():
    assert find_min([1, 2, 3, 4]) == 0


def test_find_min_all_zeros():
    assert find_min([0, 0, 0, 0]) == 0


def test_find_min_mixed_positive_negative():
    assert find_min([-1, -5, 5, 1]) == 0


def test_find_min_all_nines():
    assert find_min([9, 9, 9, 9, 9]) == 9


def test_find_min_varied_values():
    assert find_min([1, 5, 10, 3]) == 1


def test_find_min_small_mixed():
    assert find_min([-1, 0, 1]) == 0


def test_find_min_range_descending():
    assert find_min(range(10, 0, -1)) == 1


def test_find_min_large_even_partition():
    assert find_min([10, 20, 30, 40]) == 0


def test_find_min_two_elements_equal():
    assert find_min([7, 7]) == 0


def test_find_min_two_elements_different():
    assert find_min([3, 5]) == 2


def test_find_min_single_negative_raises_index_error():
    with pytest.raises(IndexError):
        find_min([-1])


def test_find_min_negative_sum_raises_index_error():
    with pytest.raises(IndexError):
        find_min([0, 0, 0, 1, 2, -4])


def test_find_min_all_negative_raises_index_error():
    with pytest.raises(IndexError):
        find_min([-1, -5, -10, -3])


def test_find_min_multiple_negatives_raises_index_error():
    with pytest.raises(IndexError):
        find_min([-10, -20, -30])


def test_find_min_large_positive_values():
    assert find_min([100, 200, 300]) == 100


def test_find_min_perfect_split():
    assert find_min([1, 1, 1, 1, 1, 1]) == 0