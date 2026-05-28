import pytest
from maths.three_sum import three_sum


def test_three_sum_basic_case():
    result = three_sum([-1, 0, 1, 2, -1, -4])
    assert sorted(result) == sorted([[-1, -1, 2], [-1, 0, 1]])


def test_three_sum_no_triplets():
    result = three_sum([1, 2, 3, 4])
    assert result == []


def test_three_sum_empty_list():
    result = three_sum([])
    assert result == []


def test_three_sum_single_element():
    result = three_sum([0])
    assert result == []


def test_three_sum_two_elements():
    result = three_sum([0, 0])
    assert result == []


def test_three_sum_all_zeros():
    result = three_sum([0, 0, 0])
    assert result == [[0, 0, 0]]


def test_three_sum_multiple_zeros():
    result = three_sum([0, 0, 0, 0])
    assert result == [[0, 0, 0]]


def test_three_sum_negative_numbers():
    result = three_sum([-5, -4, -3, -2, -1])
    assert result == []


def test_three_sum_positive_numbers():
    result = three_sum([1, 2, 3, 4, 5])
    assert result == []


def test_three_sum_mixed_with_duplicates():
    result = three_sum([-2, 0, 0, 2, 2])
    assert result == [[-2, 0, 2]]


def test_three_sum_multiple_triplets():
    result = three_sum([-4, -2, -2, -2, 0, 1, 2, 2, 2, 3, 3, 4, 4, 6, 6])
    expected = [[-4, -2, 6], [-4, 0, 4], [-4, 1, 3], [-4, 2, 2], [-2, -2, 4], [-2, 0, 2]]
    assert sorted(result) == sorted(expected)


def test_three_sum_already_sorted():
    result = three_sum([-3, -1, 0, 1, 2, 3])
    expected = [[-3, 0, 3], [-3, 1, 2], [-1, 0, 1]]
    assert sorted(result) == sorted(expected)


def test_three_sum_unsorted_input():
    result = three_sum([3, 0, -2, -1, 1, 2])
    expected = [[-2, -1, 3], [-2, 0, 2], [-1, 0, 1]]
    assert sorted(result) == sorted(expected)


def test_three_sum_large_numbers():
    result = three_sum([-100, -50, 0, 50, 100])
    assert sorted(result) == sorted([[-100, 0, 100], [-50, 0, 50]])


def test_three_sum_consecutive_duplicates():
    result = three_sum([-1, -1, -1, 0, 1, 1, 1])
    assert sorted(result) == sorted([[-1, 0, 1]])


def test_three_sum_single_triplet():
    result = three_sum([-1, 0, 1])
    assert result == [[-1, 0, 1]]


def test_three_sum_no_zero_sum():
    result = three_sum([1, 2, 3])
    assert result == []


def test_three_sum_with_zero():
    result = three_sum([-2, -1, 0, 1, 2])
    expected = [[-2, 0, 2], [-1, 0, 1]]
    assert sorted(result) == sorted(expected)