import pytest
from maths.numerical_analysis.integration_by_simpson_approx import simpson_integration

def test_simpson_integration_normal_case():
    result = simpson_integration(lambda x: x**2, 1, 2, 3)
    assert result == 2.333

def test_simpson_integration_reverse_limits():
    result = simpson_integration(lambda x: x**2, 3.45, 3.2, 1)
    assert result == -2.8

def test_simpson_integration_invalid_function():
    with pytest.raises(AssertionError, match="the function\\(object\\) passed should be callable"):
        simpson_integration('wrong_input', 2, 3, 4)

def test_simpson_integration_invalid_a():
    with pytest.raises(AssertionError, match="a should be float or integer"):
        simpson_integration(lambda x: x**2, 'wrong_input', 2, 3)

def test_simpson_integration_invalid_b():
    with pytest.raises(AssertionError, match="b should be float or integer"):
        simpson_integration(lambda x: x**2, 1, 'wrong_input', 3)

def test_simpson_integration_invalid_precision_string():
    with pytest.raises(AssertionError, match="precision should be positive integer"):
        simpson_integration(lambda x: x**2, 1, 2, 'wrong_input')

def test_simpson_integration_invalid_precision_zero():
    with pytest.raises(AssertionError, match="precision should be positive integer"):
        simpson_integration(lambda x: x**2, 3.45, 3.2, 0)

def test_simpson_integration_invalid_precision_negative():
    with pytest.raises(AssertionError, match="precision should be positive integer"):
        simpson_integration(lambda x: x**2, 3.45, 3.2, -1)