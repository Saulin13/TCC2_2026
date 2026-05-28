import pytest
from maths.numerical_analysis.newton_forward_interpolation import ucal


def test_ucal_basic_case_1():
    assert ucal(1, 2) == 0


def test_ucal_basic_case_2():
    result = ucal(1.1, 2)
    assert abs(result - 0.11) < 1e-10


def test_ucal_basic_case_3():
    result = ucal(1.2, 2)
    assert abs(result - 0.24) < 1e-10


def test_ucal_p_equals_1():
    assert ucal(5.0, 1) == 5.0
    assert ucal(2.5, 1) == 2.5
    assert ucal(-3.0, 1) == -3.0


def test_ucal_p_equals_0():
    assert ucal(5.0, 0) == 5.0
    assert ucal(0.0, 0) == 0.0
    assert ucal(-2.5, 0) == -2.5


def test_ucal_larger_p():
    result = ucal(2.0, 3)
    expected = 2.0 * (2.0 - 1) * (2.0 - 2)
    assert result == expected
    assert result == 0.0


def test_ucal_larger_p_non_integer_u():
    result = ucal(3.5, 4)
    expected = 3.5 * (3.5 - 1) * (3.5 - 2) * (3.5 - 3)
    assert abs(result - expected) < 1e-10
    assert abs(result - 6.5625) < 1e-10


def test_ucal_negative_u():
    result = ucal(-1.5, 3)
    expected = -1.5 * (-1.5 - 1) * (-1.5 - 2)
    assert abs(result - expected) < 1e-10
    assert abs(result - (-13.125)) < 1e-10


def test_ucal_zero_u():
    assert ucal(0, 2) == 0
    assert ucal(0, 5) == 0
    assert ucal(0, 1) == 0


def test_ucal_fractional_values():
    result = ucal(0.5, 3)
    expected = 0.5 * (0.5 - 1) * (0.5 - 2)
    assert abs(result - expected) < 1e-10
    assert abs(result - 0.375) < 1e-10


def test_ucal_large_p():
    result = ucal(5.0, 6)
    expected = 5.0 * 4.0 * 3.0 * 2.0 * 1.0 * 0.0
    assert result == expected
    assert result == 0.0


def test_ucal_u_between_integers():
    result = ucal(2.5, 2)
    expected = 2.5 * (2.5 - 1)
    assert abs(result - expected) < 1e-10
    assert abs(result - 3.75) < 1e-10


def test_ucal_negative_p():
    result = ucal(5.0, -1)
    assert result == 5.0


def test_ucal_negative_p_zero():
    result = ucal(3.0, -5)
    assert result == 3.0