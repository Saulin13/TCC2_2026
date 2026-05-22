import pytest
import numpy as np
from maths.numerical_analysis.runge_kutta import runge_kutta

def test_runge_kutta_normal_case():
    def f(x, y):
        return y

    y0 = 1
    x0 = 0.0
    h = 0.01
    x_end = 5
    result = runge_kutta(f, y0, x0, h, x_end)
    expected = 148.41315904125113
    assert np.isclose(result[-1], expected, rtol=1e-5)

def test_runge_kutta_edge_case_zero_step():
    def f(x, y):
        return y

    y0 = 1
    x0 = 0.0
    h = 0.01
    x_end = 0.0
    result = runge_kutta(f, y0, x0, h, x_end)
    expected = 1
    assert np.isclose(result[-1], expected, rtol=1e-5)

def test_runge_kutta_edge_case_large_step():
    def f(x, y):
        return y

    y0 = 1
    x0 = 0.0
    h = 5.0
    x_end = 5.0
    result = runge_kutta(f, y0, x0, h, x_end)
    expected = np.exp(5.0)
    assert np.isclose(result[-1], expected, rtol=1e-1)

def test_runge_kutta_exception_path():
    def f(x, y):
        return y

    y0 = 1
    x0 = 0.0
    h = 0.0
    x_end = 5.0
    with pytest.raises(ZeroDivisionError):
        runge_kutta(f, y0, x0, h, x_end)