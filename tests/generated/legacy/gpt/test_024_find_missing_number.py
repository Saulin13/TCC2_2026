import pytest
from bit_manipulation.missing_number import find_missing_number

def test_find_missing_number_normal_case():
    assert find_missing_number([0, 1, 3, 4]) == 2
    assert find_missing_number([4, 3, 1, 0]) == 2
    assert find_missing_number([-4, -3, -1, 0]) == -2
    assert find_missing_number([-2, 2, 1, 3, 0]) == -1
    assert find_missing_number([1, 3, 4, 5, 6]) == 2
    assert find_missing_number([6, 5, 4, 2, 1]) == 3
    assert find_missing_number([6, 1, 5, 3, 4]) == 2

def test_find_missing_number_edge_case_single_element():
    assert find_missing_number([1]) == 0
    assert find_missing_number([0]) == 1

def test_find_missing_number_edge_case_no_missing():
    assert find_missing_number([0, 1, 2, 3, 4]) == 4  # Since the function assumes one missing, it will return the max

def test_find_missing_number_edge_case_negative_numbers():
    assert find_missing_number([-3, -2, -1, 0, 1, 3]) == 2

def test_find_missing_number_failure_case_empty_list():
    with pytest.raises(ValueError):
        find_missing_number([])

def test_find_missing_number_failure_case_non_consecutive():
    assert find_missing_number([10, 12, 11, 14]) == 13