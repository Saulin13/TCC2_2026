import pytest
from maths.numerical_analysis.integration_by_simpson_approx import simpson_integration

def test_simpson_integration_normal_case():
    assert simpson_integration(lambda x: x**2, 1, 2, 3) == 2.333
    assert simpson_integration(lambda x: x**3, 0, 1, 4) == 0.25
    assert simpson_integration(lambda x: x, 0, 10, 2) == 50.0

def test_simpson_integration_edge_case():
    assert simpson_integration(lambda x: x**2, 3.45, 3.2, 1) == -2.8

def test_simpson_integration_invalid_function():
    with pytest.raises(AssertionError, match="the function\\(object\\) passed should be callable"):
        simpson_integration('wrong_input', 2, 3, 4)

def test_simpson_integration_invalid_a():
    with pytest.raises(AssertionError, match="a should be float or integer"):
        simpson_integration(lambda x: x**2, 'wrong_input', 2, 3)

def test_simpson_integration_invalid_b():
    with pytest.raises(AssertionError, match="b should be float or integer"):
        simpson_integration(lambda x: x**2, 1, 'wrong_input', 3)

def test_simpson_integration_invalid_precision():
    with pytest.raises(AssertionError, match="precision should be positive integer"):
        simpson_integration(lambda x: x**2, 1, 2, 'wrong_input')
    with pytest.raises(AssertionError, match="precision should be positive integer"):
        simpson_integration(lambda x: x**2, 1, 2, 0)
    with pytest.raises(AssertionError, match="precision should be positive integer"):
        simpson_integration(lambda x: x**2, 1, 2, -1)