import pytest
from bit_manipulation.find_unique_number import find_unique_number

def test_find_unique_number_normal_cases():
    assert find_unique_number([1, 1, 2, 2, 3]) == 3
    assert find_unique_number([4, 5, 4, 6, 6]) == 5
    assert find_unique_number([10, 20, 10]) == 20
    assert find_unique_number([7]) == 7

def test_find_unique_number_edge_cases():
    assert find_unique_number([0, 1, 1]) == 0
    assert find_unique_number([-1, -1, -2]) == -2
    assert find_unique_number([0, 0, 0, 0, 0, 0, 0, 1]) == 1

def test_find_unique_number_empty_list():
    with pytest.raises(ValueError, match="input list must not be empty"):
        find_unique_number([])

def test_find_unique_number_non_integer_elements():
    with pytest.raises(TypeError, match="all elements must be integers"):
        find_unique_number([1, 'a', 1])
    with pytest.raises(TypeError, match="all elements must be integers"):
        find_unique_number([1, 2.5, 1])
    with pytest.raises(TypeError, match="all elements must be integers"):
        find_unique_number([1, None, 1])