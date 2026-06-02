import pytest
import numpy as np
from sklearn.metrics._regression import mean_tweedie_deviance


def test_mean_tweedie_deviance_power_0_normal():
    y_true = np.array([1.0, 2.0, 3.0, 4.0])
    y_pred = np.array([1.5, 2.5, 2.5, 3.5])
    result = mean_tweedie_deviance(y_true, y_pred, power=0)
    assert isinstance(result, float)
    assert result >= 0.0


def test_mean_tweedie_deviance_power_1_poisson():
    y_true = np.array([2, 0, 1, 4])
    y_pred = np.array([0.5, 0.5, 2.0, 2.0])
    result = mean_tweedie_deviance(y_true, y_pred, power=1)
    assert isinstance(result, float)
    assert result >= 0.0
    assert abs(result - 1.4260) < 0.01


def test_mean_tweedie_deviance_power_2_gamma():
    y_true = np.array([1.0, 2.0, 3.0, 4.0])
    y_pred = np.array([1.5, 2.5, 2.5, 3.5])
    result = mean_tweedie_deviance(y_true, y_pred, power=2)
    assert isinstance(result, float)
    assert result >= 0.0


def test_mean_tweedie_deviance_power_3_inverse_gaussian():
    y_true = np.array([1.0, 2.0, 3.0, 4.0])
    y_pred = np.array([1.5, 2.5, 2.5, 3.5])
    result = mean_tweedie_deviance(y_true, y_pred, power=3)
    assert isinstance(result, float)
    assert result >= 0.0


def test_mean_tweedie_deviance_with_sample_weight():
    y_true = np.array([1.0, 2.0, 3.0, 4.0])
    y_pred = np.array([1.5, 2.5, 2.5, 3.5])
    sample_weight = np.array([1.0, 2.0, 1.0, 1.0])
    result = mean_tweedie_deviance(y_true, y_pred, sample_weight=sample_weight, power=0)
    assert isinstance(result, float)
    assert result >= 0.0


def test_mean_tweedie_deviance_perfect_prediction():
    y_true = np.array([1.0, 2.0, 3.0, 4.0])
    y_pred = np.array([1.0, 2.0, 3.0, 4.0])
    result = mean_tweedie_deviance(y_true, y_pred, power=0)
    assert result == 0.0


def test_mean_tweedie_deviance_power_negative():
    y_true = np.array([1.0, 2.0, 3.0, 4.0])
    y_pred = np.array([1.5, 2.5, 2.5, 3.5])
    result = mean_tweedie_deviance(y_true, y_pred, power=-1)
    assert isinstance(result, float)
    assert result >= 0.0


def test_mean_tweedie_deviance_power_1_5_compound_poisson():
    y_true = np.array([1.0, 2.0, 3.0, 4.0])
    y_pred = np.array([1.5, 2.5, 2.5, 3.5])
    result = mean_tweedie_deviance(y_true, y_pred, power=1.5)
    assert isinstance(result, float)
    assert result >= 0.0


def test_mean_tweedie_deviance_power_negative_invalid_y_pred():
    y_true = np.array([1.0, 2.0, 3.0, 4.0])
    y_pred = np.array([1.5, -0.5, 2.5, 3.5])
    with pytest.raises(ValueError, match="strictly positive y_pred"):
        mean_tweedie_deviance(y_true, y_pred, power=-1)


def test_mean_tweedie_deviance_power_1_negative_y_true():
    y_true = np.array([-1.0, 2.0, 3.0, 4.0])
    y_pred = np.array([1.5, 2.5, 2.5, 3.5])
    with pytest.raises(ValueError, match="non-negative y and strictly positive y_pred"):
        mean_tweedie_deviance(y_true, y_pred, power=1)


def test_mean_tweedie_deviance_power_1_non_positive_y_pred():
    y_true = np.array([1.0, 2.0, 3.0, 4.0])
    y_pred = np.array([1.5, 0.0, 2.5, 3.5])
    with pytest.raises(ValueError, match="non-negative y and strictly positive y_pred"):
        mean_tweedie_deviance(y_true, y_pred, power=1)


def test_mean_tweedie_deviance_power_2_non_positive_y_true():
    y_true = np.array([0.0, 2.0, 3.0, 4.0])
    y_pred = np.array([1.5, 2.5, 2.5, 3.5])
    with pytest.raises(ValueError, match="strictly positive y and y_pred"):
        mean_tweedie_deviance(y_true, y_pred, power=2)


def test_mean_tweedie_deviance_power_2_non_positive_y_pred():
    y_true = np.array([1.0, 2.0, 3.0, 4.0])
    y_pred = np.array([1.5, 0.0, 2.5, 3.5])
    with pytest.raises(ValueError, match="strictly positive y and y_pred"):
        mean_tweedie_deviance(y_true, y_pred, power=2)


def test_mean_tweedie_deviance_multioutput_not_supported():
    y_true = np.array([[1.0, 2.0], [3.0, 4.0]])
    y_pred = np.array([[1.5, 2.5], [2.5, 3.5]])
    with pytest.raises(ValueError, match="Multioutput not supported"):
        mean_tweedie_deviance(y_true, y_pred, power=0)


def test_mean_tweedie_deviance_single_sample():
    y_true = np.array([2.0])
    y_pred = np.array([1.5])
    result = mean_tweedie_deviance(y_true, y_pred, power=0)
    assert isinstance(result, float)
    assert result >= 0.0


def test_mean_tweedie_deviance_lists_as_input():
    y_true = [1.0, 2.0, 3.0, 4.0]
    y_pred = [1.5, 2.5, 2.5, 3.5]
    result = mean_tweedie_deviance(y_true, y_pred, power=0)
    assert isinstance(result, float)
    assert result >= 0.0