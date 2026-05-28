import pytest
from sorts.dutch_national_flag_sort import dutch_national_flag_sort


def test_empty_list():
    assert dutch_national_flag_sort([]) == []


def test_single_element_zero():
    assert dutch_national_flag_sort([0]) == [0]


def test_single_element_one():
    assert dutch_national_flag_sort([1]) == [1]


def test_single_element_two():
    assert dutch_national_flag_sort([2]) == [2]


def test_two_elements_sorted():
    assert dutch_national_flag_sort([0, 1]) == [0, 1]


def test_two_elements_unsorted():
    assert dutch_national_flag_sort([1, 0]) == [0, 1]


def test_basic_unsorted():
    assert dutch_national_flag_sort([2, 1, 0, 0, 1, 2]) == [0, 0, 1, 1, 2, 2]


def test_longer_sequence():
    assert dutch_national_flag_sort([0, 1, 1, 0, 1, 2, 1, 2, 0, 0, 0, 1]) == [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2]


def test_all_zeros():
    assert dutch_national_flag_sort([0, 0, 0, 0]) == [0, 0, 0, 0]


def test_all_ones():
    assert dutch_national_flag_sort([1, 1, 1, 1]) == [1, 1, 1, 1]


def test_all_twos():
    assert dutch_national_flag_sort([2, 2, 2, 2]) == [2, 2, 2, 2]


def test_already_sorted():
    assert dutch_national_flag_sort([0, 0, 1, 1, 2, 2]) == [0, 0, 1, 1, 2, 2]


def test_reverse_sorted():
    assert dutch_national_flag_sort([2, 2, 1, 1, 0, 0]) == [0, 0, 1, 1, 2, 2]


def test_only_zeros_and_ones():
    assert dutch_national_flag_sort([1, 0, 1, 0, 1, 0]) == [0, 0, 0, 1, 1, 1]


def test_only_zeros_and_twos():
    assert dutch_national_flag_sort([2, 0, 2, 0, 2, 0]) == [0, 0, 0, 2, 2, 2]


def test_only_ones_and_twos():
    assert dutch_national_flag_sort([2, 1, 2, 1, 2, 1]) == [1, 1, 1, 2, 2, 2]


def test_invalid_value_three():
    with pytest.raises(ValueError, match="The elements inside the sequence must contains only"):
        dutch_national_flag_sort([3, 2, 3, 1, 3, 0, 3])


def test_invalid_value_negative():
    with pytest.raises(ValueError, match="The elements inside the sequence must contains only"):
        dutch_national_flag_sort([-1, 2, -1, 1, -1, 0, -1])


def test_invalid_value_float():
    with pytest.raises(ValueError, match="The elements inside the sequence must contains only"):
        dutch_national_flag_sort([1.1, 2, 1.1, 1, 1.1, 0, 1.1])


def test_invalid_string_lowercase():
    with pytest.raises(ValueError, match="The elements inside the sequence must contains only"):
        dutch_national_flag_sort("abacab")


def test_invalid_string_mixed_case():
    with pytest.raises(ValueError, match="The elements inside the sequence must contains only"):
        dutch_national_flag_sort("Abacab")


def test_invalid_value_four():
    with pytest.raises(ValueError, match="The elements inside the sequence must contains only"):
        dutch_national_flag_sort([0, 1, 2, 4])


def test_mixed_valid_and_invalid():
    with pytest.raises(ValueError, match="The elements inside the sequence must contains only"):
        dutch_national_flag_sort([0, 1, 2, 3, 1, 0])