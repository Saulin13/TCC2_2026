import pytest
from bit_manipulation.find_unique_number import find_unique_number


def test_find_unique_number_basic_case():
    assert find_unique_number([1, 1, 2, 2, 3]) == 3


def test_find_unique_number_different_order():
    assert find_unique_number([4, 5, 4, 6, 6]) == 5


def test_find_unique_number_single_element():
    assert find_unique_number([7]) == 7


def test_find_unique_number_unique_at_start():
    assert find_unique_number([10, 20, 10]) == 20


def test_find_unique_number_unique_at_end():
    assert find_unique_number([5, 5, 8, 8, 9]) == 9


def test_find_unique_number_larger_list():
    assert find_unique_number([1, 2, 3, 4, 5, 1, 2, 3, 4]) == 5


def test_find_unique_number_negative_numbers():
    assert find_unique_number([-1, -1, -2, -2, -3]) == -3


def test_find_unique_number_mixed_positive_negative():
    assert find_unique_number([10, -10, 10, 5, -10]) == 5


def test_find_unique_number_zero_unique():
    assert find_unique_number([0, 1, 1, 2, 2]) == 0


def test_find_unique_number_zero_duplicates():
    assert find_unique_number([0, 0, 5]) == 5


def test_find_unique_number_large_numbers():
    assert find_unique_number([1000000, 1000000, 999999]) == 999999


def test_find_unique_number_empty_list_raises_value_error():
    with pytest.raises(ValueError, match="input list must not be empty"):
        find_unique_number([])


def test_find_unique_number_string_element_raises_type_error():
    with pytest.raises(TypeError, match="all elements must be integers"):
        find_unique_number([1, 'a', 1])


def test_find_unique_number_float_element_raises_type_error():
    with pytest.raises(TypeError, match="all elements must be integers"):
        find_unique_number([1, 1.5, 1])


def test_find_unique_number_none_element_raises_type_error():
    with pytest.raises(TypeError, match="all elements must be integers"):
        find_unique_number([1, None, 1])


def test_find_unique_number_mixed_types_raises_type_error():
    with pytest.raises(TypeError, match="all elements must be integers"):
        find_unique_number([1, 2, 2, 'string'])


def test_find_unique_number_boolean_raises_type_error():
    with pytest.raises(TypeError, match="all elements must be integers"):
        find_unique_number([1, True, 1])
```