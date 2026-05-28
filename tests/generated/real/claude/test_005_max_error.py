import pytest
import numpy as np
from sklearn.metrics._regression import max_error


def test_max_error_basic():
    y_true = [3, 2, 7, 1]
    y_pred = [4, 2, 7, 1]
    result = max_error(y_true, y_pred)
    assert result == 1.0


def test_max_error_all_correct():
    y_true = [1, 2, 3, 4, 5]
    y_pred = [1, 2, 3, 4, 5]
    result = max_error(y_true, y_pred)
    assert result == 0.0


def test_max_error_negative_residuals():
    y_true = [10, 20, 30, 40]
    y_pred = [15, 18, 35, 38]
    result = max_error(y_true, y_pred)
    assert result == 5.0


def test_max_error_mixed_residuals():
    y_true = [1, 5, 10, 15]
    y_pred = [3, 4, 12, 10]
    result = max_error(y_true, y_pred)
    assert result == 5.0


def test_max_error_single_value():
    y_true = [5]
    y_pred = [8]
    result = max_error(y_true, y_pred)
    assert result == 3.0


def test_max_error_numpy_arrays():
    y_true = np.array([1.5, 2.5, 3.5, 4.5])
    y_pred = np.array([1.0, 2.0, 4.0, 4.0])
    result = max_error(y_true, y_pred)
    assert result == 0.5


def test_max_error_floats():
    y_true = [1.1, 2.2, 3.3, 4.4]
    y_pred = [1.0, 2.0, 3.0, 4.0]
    result = max_error(y_true, y_pred)
    assert pytest.approx(result, abs=1e-7) == 0.4


def test_max_error_large_errors():
    y_true = [0, 100, 200]
    y_pred = [50, 150, 100]
    result = max_error(y_true, y_pred)
    assert result == 100.0


def test_max_error_negative_values():
    y_true = [-10, -5, 0, 5, 10]
    y_pred = [-8, -7, 2, 3, 12]
    result = max_error(y_true, y_pred)
    assert result == 2.0


def test_max_error_multioutput_raises():
    y_true = [[1, 2], [3, 4], [5, 6]]
    y_pred = [[1, 2], [3, 5], [5, 6]]
    with pytest.raises(ValueError, match="Multioutput not supported in max_error"):
        max_error(y_true, y_pred)


def test_max_error_2d_single_output():
    y_true = np.array([[1], [2], [3], [4]])
    y_pred = np.array([[1.5], [2.5], [3.5], [4.5]])
    result = max_error(y_true, y_pred)
    assert result == 0.5


def test_max_error_symmetric():
    y_true = [1, 2, 3, 4]
    y_pred = [2, 3, 4, 5]
    result1 = max_error(y_true, y_pred)
    result2 = max_error(y_pred, y_true)
    assert result1 == result2 == 1.0


def test_max_error_zeros():
    y_true = [0, 0, 0, 0]
    y_pred = [1, -2, 3, -1]
    result = max_error(y_true, y_pred)
    assert result == 3.0