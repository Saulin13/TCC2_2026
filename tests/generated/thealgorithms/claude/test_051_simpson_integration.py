import pytest
from maths.numerical_analysis.integration_by_simpson_approx import simpson_integration


def test_simpson_integration_basic_quadratic():
    result = simpson_integration(lambda x: x * x, 1, 2, 3)
    assert result == 2.333


def test_simpson_integration_linear_function():
    result = simpson_integration(lambda x: 2 * x, 0, 1, 4)
    assert result == 1.0


def test_simpson_integration_constant_function():
    result = simpson_integration(lambda x: 5, 0, 10, 2)
    assert result == 50.0


def test_simpson_integration_cubic_function():
    result = simpson_integration(lambda x: x ** 3, 0, 2, 2)
    assert result == 4.0


def test_simpson_integration_sine_function():
    import math
    result = simpson_integration(math.sin, 0, math.pi, 4)
    assert abs(result - 2.0) < 0.01


def test_simpson_integration_reversed_limits():
    result = simpson_integration(lambda x: x * x, 3.45, 3.2, 1)
    assert result == -2.8


def test_simpson_integration_negative_range():
    result = simpson_integration(lambda x: x * x, -2, -1, 3)
    assert result == 2.333


def test_simpson_integration_zero_range():
    result = simpson_integration(lambda x: x * x, 5, 5, 2)
    assert result == 0.0


def test_simpson_integration_float_limits():
    result = simpson_integration(lambda x: x, 1.5, 2.5, 2)
    assert result == 2.0


def test_simpson_integration_high_precision():
    result = simpson_integration(lambda x: x * x, 0, 1, 10)
    assert isinstance(result, float)
    assert abs(result - 0.3333333333) < 1e-9


def test_simpson_integration_low_precision():
    result = simpson_integration(lambda x: x * x, 0, 1, 1)
    assert result == 0.3


def test_simpson_integration_non_callable_function():
    with pytest.raises(AssertionError, match="the function\\(object\\) passed should be callable"):
        simpson_integration('wrong_input', 2, 3, 4)


def test_simpson_integration_invalid_a_string():
    with pytest.raises(AssertionError, match="a should be float or integer"):
        simpson_integration(lambda x: x * x, 'wrong_input', 2, 3)


def test_simpson_integration_invalid_b_string():
    with pytest.raises(AssertionError, match="b should be float or integer"):
        simpson_integration(lambda x: x * x, 1, 'wrong_input', 3)


def test_simpson_integration_invalid_precision_string():
    with pytest.raises(AssertionError, match="precision should be positive integer"):
        simpson_integration(lambda x: x * x, 1, 2, 'wrong_input')


def test_simpson_integration_invalid_precision_zero():
    with pytest.raises(AssertionError, match="precision should be positive integer"):
        simpson_integration(lambda x: x * x, 3.45, 3.2, 0)


def test_simpson_integration_invalid_precision_negative():
    with pytest.raises(AssertionError, match="precision should be positive integer"):
        simpson_integration(lambda x: x * x, 3.45, 3.2, -1)


def test_simpson_integration_invalid_precision_float():
    with pytest.raises(AssertionError, match="precision should be positive integer"):
        simpson_integration(lambda x: x * x, 1, 2, 3.5)


def test_simpson_integration_invalid_a_none():
    with pytest.raises(AssertionError, match="a should be float or integer"):
        simpson_integration(lambda x: x * x, None, 2, 3)


def test_simpson_integration_invalid_b_none():
    with pytest.raises(AssertionError, match="b should be float or integer"):
        simpson_integration(lambda x: x * x, 1, None, 3)


def test_simpson_integration_function_returns_non_numeric():
    with pytest.raises(AssertionError, match="the function should return integer or float"):
        simpson_integration(lambda x: "string", 1, 2, 3)


def test_simpson_integration_exponential_function():
    import math
    result = simpson_integration(math.exp, 0, 1, 4)
    assert abs(result - (math.e - 1)) < 0.01


def test_simpson_integration_integer_limits():
    result = simpson_integration(lambda x: x ** 2, 0, 3, 2)
    assert result == 9.0