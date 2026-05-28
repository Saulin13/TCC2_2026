import pytest
import numpy as np
from sklearn.metrics._regression import mean_tweedie_deviance

def test_mean_tweedie_deviance_normal_case():
    y_true = np.array([2, 0, 1, 4])
    y_pred = np.array([0.5, 0.5, 2., 2.])
    result = mean_tweedie_deviance(y_true, y_pred, power=1)
    expected = 1.4260
    assert pytest.approx(result, 0.001) == expected

def test_mean_tweedie_deviance_power_zero():
    y_true = np.array([2, -1, 1, 4])
    y_pred = np.array([2, -1, 1, 4])
    result = mean_tweedie_deviance(y_true, y_pred, power=0)
    expected = 0.0
    assert result == expected

def test_mean_tweedie_deviance_poisson():
    y_true = np.array([2, 0, 1, 4])
    y_pred = np.array([1, 1, 1, 1])
    result = mean_tweedie_deviance(y_true, y_pred, power=1)
    expected = 1.5
    assert pytest.approx(result, 0.001) == expected

def test_mean_tweedie_deviance_gamma():
    y_true = np.array([2, 1, 1, 4])
    y_pred = np.array([1, 1, 1, 1])
    result = mean_tweedie_deviance(y_true, y_pred, power=2)
    expected = 1.5
    assert pytest.approx(result, 0.001) == expected

def test_mean_tweedie_deviance_invalid_y_pred():
    y_true = np.array([2, 0, 1, 4])
    y_pred = np.array([-1, 0.5, 2., 2.])
    with pytest.raises(ValueError, match="strictly positive y_pred"):
        mean_tweedie_deviance(y_true, y_pred, power=1)

def test_mean_tweedie_deviance_invalid_y_true():
    y_true = np.array([-1, 0, 1, 4])
    y_pred = np.array([0.5, 0.5, 2., 2.])
    with pytest.raises(ValueError, match="non-negative y and strictly positive y_pred"):
        mean_tweedie_deviance(y_true, y_pred, power=1)

def test_mean_tweedie_deviance_sample_weight():
    y_true = np.array([2, 0, 1, 4])
    y_pred = np.array([0.5, 0.5, 2., 2.])
    sample_weight = np.array([1, 0, 1, 0])
    result = mean_tweedie_deviance(y_true, y_pred, power=1, sample_weight=sample_weight)
    expected = 1.0
    assert pytest.approx(result, 0.001) == expected