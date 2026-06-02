import pytest
import numpy as np
from sklearn.metrics._regression import mean_tweedie_deviance

def test_mean_tweedie_deviance_normal_case():
    y_true = [2, 0, 1, 4]
    y_pred = [0.5, 0.5, 2.0, 2.0]
    result = mean_tweedie_deviance(y_true, y_pred, power=1)
    expected = 1.4260  # Expected value from the example
    assert np.isclose(result, expected, atol=1e-4)

def test_mean_tweedie_deviance_power_zero():
    y_true = [2, -1, 1, 4]
    y_pred = [0.5, 0.5, 2.0, 2.0]
    result = mean_tweedie_deviance(y_true, y_pred, power=0)
    expected = np.mean((np.array(y_true) - np.array(y_pred)) ** 2)
    assert np.isclose(result, expected, atol=1e-4)

def test_mean_tweedie_deviance_power_two():
    y_true = [2, 1, 1, 4]
    y_pred = [0.5, 0.5, 2.0, 2.0]
    with pytest.raises(ValueError, match="strictly positive y and y_pred"):
        mean_tweedie_deviance(y_true, y_pred, power=2)

def test_mean_tweedie_deviance_negative_power():
    y_true = [2, 1, 1, 4]
    y_pred = [0.5, 0.5, 2.0, 2.0]
    with pytest.raises(ValueError, match="strictly positive y_pred"):
        mean_tweedie_deviance(y_true, y_pred, power=-1)

def test_mean_tweedie_deviance_poisson_distribution():
    y_true = [2, 0, 1, 4]
    y_pred = [0.5, 0.5, 2.0, 2.0]
    result = mean_tweedie_deviance(y_true, y_pred, power=1)
    expected = 1.4260  # Expected value from the example
    assert np.isclose(result, expected, atol=1e-4)

def test_mean_tweedie_deviance_gamma_distribution():
    y_true = [2, 1, 1, 4]
    y_pred = [0.5, 0.5, 2.0, 2.0]
    with pytest.raises(ValueError, match="strictly positive y and y_pred"):
        mean_tweedie_deviance(y_true, y_pred, power=2)

def test_mean_tweedie_deviance_edge_case_zero_values():
    y_true = [0, 0, 0, 0]
    y_pred = [0, 0, 0, 0]
    result = mean_tweedie_deviance(y_true, y_pred, power=0)
    expected = 0.0
    assert np.isclose(result, expected, atol=1e-4)

def test_mean_tweedie_deviance_sample_weight():
    y_true = [2, 0, 1, 4]
    y_pred = [0.5, 0.5, 2.0, 2.0]
    sample_weight = [1, 1, 1, 1]
    result = mean_tweedie_deviance(y_true, y_pred, power=1, sample_weight=sample_weight)
    expected = 1.4260  # Expected value from the example
    assert np.isclose(result, expected, atol=1e-4)