import pytest
from dynamic_programming.longest_increasing_subsequence import longest_subsequence


def test_longest_subsequence_normal_case_1():
    assert longest_subsequence([10, 22, 9, 33, 21, 50, 41, 60, 80]) == [10, 22, 33, 41, 60, 80]


def test_longest_subsequence_normal_case_2():
    assert longest_subsequence([4, 8, 7, 5, 1, 12, 2, 3, 9]) == [1, 2, 3, 9]


def test_longest_subsequence_normal_case_3():
    assert longest_subsequence([28, 26, 12, 23, 35, 39]) == [12, 23, 35, 39]


def test_longest_subsequence_with_duplicates():
    assert longest_subsequence([9, 8, 7, 6, 5, 7]) == [5, 7]


def test_longest_subsequence_all_same_elements():
    assert longest_subsequence([1, 1, 1]) == [1, 1, 1]


def test_longest_subsequence_empty_array():
    assert longest_subsequence([]) == []


def test_longest_subsequence_single_element():
    assert longest_subsequence([5]) == [5]


def test_longest_subsequence_two_elements_increasing():
    assert longest_subsequence([1, 2]) == [1, 2]


def test_longest_subsequence_two_elements_decreasing():
    assert longest_subsequence([2, 1]) == [1]


def test_longest_subsequence_strictly_increasing():
    assert longest_subsequence([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]


def test_longest_subsequence_strictly_decreasing():
    assert longest_subsequence([5, 4, 3, 2, 1]) == [1]


def test_longest_subsequence_with_negative_numbers():
    assert longest_subsequence([-5, -2, -8, -1, 0, 3]) == [-5, -2, -1, 0, 3]


def test_longest_subsequence_mixed_positive_negative():
    assert longest_subsequence([3, -1, 4, -2, 5, 1, 6]) == [-2, 1, 6]


def test_longest_subsequence_with_zeros():
    assert longest_subsequence([0, 1, 0, 2, 0, 3]) == [0, 1, 2, 3]


def test_longest_subsequence_large_numbers():
    assert longest_subsequence([100, 200, 50, 300, 400]) == [100, 200, 300, 400]


def test_longest_subsequence_duplicate_values_at_start():
    assert longest_subsequence([5, 5, 6, 7, 8]) == [5, 6, 7, 8]


def test_longest_subsequence_alternating_pattern():
    assert longest_subsequence([1, 10, 2, 11, 3, 12]) == [1, 2, 3, 12]


def test_longest_subsequence_type_error_none():
    with pytest.raises(TypeError):
        longest_subsequence(None)


def test_longest_subsequence_type_error_string():
    with pytest.raises(TypeError):
        longest_subsequence("not a list")


def test_longest_subsequence_type_error_non_int_elements():
    with pytest.raises(TypeError):
        longest_subsequence([1, 2, "3", 4])