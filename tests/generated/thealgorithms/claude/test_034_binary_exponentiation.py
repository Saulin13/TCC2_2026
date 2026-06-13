import pytest
from maths.fermat_little_theorem import binary_exponentiation


def test_binary_exponentiation_zero_exponent():
    assert binary_exponentiation(5, 0, 13) == 1
    assert binary_exponentiation(100, 0, 7) == 1
    assert binary_exponentiation(1, 0, 1000) == 1


def test_binary_exponentiation_exponent_one():
    assert binary_exponentiation(5, 1, 13) == 5
    assert binary_exponentiation(7, 1, 10) == 7
    assert binary_exponentiation(100, 1, 97) == 3


def test_binary_exponentiation_small_values():
    assert binary_exponentiation(2, 3, 5) == 3
    assert binary_exponentiation(3, 4, 7) == 4
    assert binary_exponentiation(5, 2, 13) == 12


def test_binary_exponentiation_even_exponent():
    assert binary_exponentiation(2, 10, 1000) == 24
    assert binary_exponentiation(3, 8, 100) == 61
    assert binary_exponentiation(5, 4, 13) == 1


def test_binary_exponentiation_odd_exponent():
    assert binary_exponentiation(2, 5, 13) == 6
    assert binary_exponentiation(3, 7, 11) == 9
    assert binary_exponentiation(7, 3, 10) == 3


def test_binary_exponentiation_large_values():
    assert binary_exponentiation(2, 100, 1000000007) == 976371285
    assert binary_exponentiation(123, 456, 789) == 699
    assert binary_exponentiation(10, 50, 97) == 88


def test_binary_exponentiation_base_zero():
    assert binary_exponentiation(0, 5, 7) == 0
    assert binary_exponentiation(0, 100, 13) == 0


def test_binary_exponentiation_base_one():
    assert binary_exponentiation(1, 1000, 7) == 1
    assert binary_exponentiation(1, 999, 13) == 1


def test_binary_exponentiation_modulo_one():
    assert binary_exponentiation(5, 3, 1) == 0
    assert binary_exponentiation(100, 50, 1) == 0


def test_binary_exponentiation_base_greater_than_mod():
    assert binary_exponentiation(15, 3, 7) == 6
    assert binary_exponentiation(20, 5, 13) == 7


def test_binary_exponentiation_result_equals_mod():
    assert binary_exponentiation(7, 1, 7) == 0
    assert binary_exponentiation(13, 2, 13) == 0


def test_binary_exponentiation_float_exponent_even():
    assert binary_exponentiation(2, 4.0, 13) == 3
    assert binary_exponentiation(3, 6.0, 11) == 3


def test_binary_exponentiation_type_error_invalid_exponent():
    with pytest.raises((TypeError, RecursionError)):
        binary_exponentiation(2, 3.5, 13)


def test_binary_exponentiation_recursion_error_negative_exponent():
    with pytest.raises(RecursionError):
        binary_exponentiation(2, -5, 13)