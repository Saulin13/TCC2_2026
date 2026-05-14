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
    expected = np.exp(x_end)
    assert pytest.approx(result[-1], rel=1e-5) == expected

def test_runge_kutta_edge_case_zero_step_size():
    def f(x, y):
        return y

    y0 = 1
    x0 = 0.0
    h = 0.0
    x_end = 5
    with pytest.raises(ZeroDivisionError):
        runge_kutta(f, y0, x0, h, x_end)

def test_runge_kutta_edge_case_zero_interval():
    def f(x, y):
        return y

    y0 = 1
    x0 = 0.0
    h = 0.01
    x_end = 0.0
    result = runge_kutta(f, y0, x0, h, x_end)
    assert len(result) == 1
    assert result[0] == y0

def test_runge_kutta_failure_case_invalid_function():
    y0 = 1
    x0 = 0.0
    h = 0.01
    x_end = 5
    with pytest.raises(TypeError):
        runge_kutta(None, y0, x0, h, x_end)