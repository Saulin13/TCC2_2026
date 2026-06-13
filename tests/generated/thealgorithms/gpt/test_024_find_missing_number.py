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

def test_find_missing_number_edge_case():
    assert find_missing_number([0]) == 1
    assert find_missing_number([1]) == 0
    assert find_missing_number([-1, 0, 1, 2, 3, 5]) == 4
    assert find_missing_number([100, 101, 102, 104]) == 103

def test_find_missing_number_failure_case():
    with pytest.raises(ValueError):
        find_missing_number([])  # Assuming the function should raise an error for empty list