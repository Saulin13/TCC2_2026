import pytest
from bit_manipulation.find_unique_number import find_unique_number

def test_find_unique_number_normal_cases():
    assert find_unique_number([1, 1, 2, 2, 3]) == 3
    assert find_unique_number([4, 5, 4, 6, 6]) == 5
    assert find_unique_number([10, 20, 10]) == 20

def test_find_unique_number_single_element():
    assert find_unique_number([7]) == 7

def test_find_unique_number_empty_list():
    with pytest.raises(ValueError, match="input list must not be empty"):
        find_unique_number([])

def test_find_unique_number_non_integer_elements():
    with pytest.raises(TypeError, match="all elements must be integers"):
        find_unique_number([1, 'a', 1])

def test_find_unique_number_all_elements_twice():
    with pytest.raises(ValueError, match="input list must not be empty"):
        find_unique_number([2, 2, 3, 3])