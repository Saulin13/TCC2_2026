import pytest
from sorts.dutch_national_flag_sort import dutch_national_flag_sort

def test_empty_list():
    assert dutch_national_flag_sort([]) == []

def test_single_element():
    assert dutch_national_flag_sort([0]) == [0]
    assert dutch_national_flag_sort([1]) == [1]
    assert dutch_national_flag_sort([2]) == [2]

def test_sorted_list():
    assert dutch_national_flag_sort([0, 0, 1, 1, 2, 2]) == [0, 0, 1, 1, 2, 2]

def test_reverse_sorted_list():
    assert dutch_national_flag_sort([2, 2, 1, 1, 0, 0]) == [0, 0, 1, 1, 2, 2]

def test_unsorted_list():
    assert dutch_national_flag_sort([2, 1, 0, 0, 1, 2]) == [0, 0, 1, 1, 2, 2]
    assert dutch_national_flag_sort([0, 1, 1, 0, 1, 2, 1, 2, 0, 0, 0, 1]) == [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2]

def test_invalid_elements():
    with pytest.raises(ValueError, match=r"The elements inside the sequence must contains only \(0, 1, 2\) values"):
        dutch_national_flag_sort("abacab")
    with pytest.raises(ValueError, match=r"The elements inside the sequence must contains only \(0, 1, 2\) values"):
        dutch_national_flag_sort("Abacab")
    with pytest.raises(ValueError, match=r"The elements inside the sequence must contains only \(0, 1, 2\) values"):
        dutch_national_flag_sort([3, 2, 3, 1, 3, 0, 3])
    with pytest.raises(ValueError, match=r"The elements inside the sequence must contains only \(0, 1, 2\) values"):
        dutch_national_flag_sort([-1, 2, -1, 1, -1, 0, -1])
    with pytest.raises(ValueError, match=r"The elements inside the sequence must contains only \(0, 1, 2\) values"):
        dutch_national_flag_sort([1.1, 2, 1.1, 1, 1.1, 0, 1.1])