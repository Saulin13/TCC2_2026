import pytest
import numpy as np
from sklearn.metrics._classification import d2_log_loss_score
from sklearn.exceptions import UndefinedMetricWarning

def test_d2_log_loss_score_basic():
    y_true = [0, 1, 0, 1]
    y_proba = [[0.9, 0.1], [0.2, 0.8], [0.8, 0.2], [0.3, 0.7]]
    score = d2_log_loss_score(y_true, y_proba=y_proba)
    assert 0 <= score <= 1

def test_d2_log_loss_score_perfect_prediction():
    y_true = [0, 1, 0, 1]
    y_proba = [[1.0, 0.0], [0.0, 1.0], [1.0, 0.0], [0.0, 1.0]]
    score = d2_log_loss_score(y_true, y_proba=y_proba)
    assert score == 1.0

def test_d2_log_loss_score_worst_prediction():
    y_true = [0, 1, 0, 1]
    y_proba = [[0.0, 1.0], [1.0, 0.0], [0.0, 1.0], [1.0, 0.0]]
    score = d2_log_loss_score(y_true, y_proba=y_proba)
    assert score < 0

def test_d2_log_loss_score_single_sample():
    y_true = [0]
    y_proba = [[0.9, 0.1]]
    with pytest.warns(UndefinedMetricWarning, match="D^2 score is not well-defined with less than two samples."):
        score = d2_log_loss_score(y_true, y_proba=y_proba)
    assert np.isnan(score)

def test_d2_log_loss_score_binary_probabilities():
    y_true = [0, 1, 0, 1]
    y_proba = [0.9, 0.8, 0.8, 0.7]
    score = d2_log_loss_score(y_true, y_proba=y_proba)
    assert 0 <= score <= 1

def test_d2_log_loss_score_with_sample_weight():
    y_true = [0, 1, 0, 1]
    y_proba = [[0.9, 0.1], [0.2, 0.8], [0.8, 0.2], [0.3, 0.7]]
    sample_weight = [1, 2, 1, 2]
    score = d2_log_loss_score(y_true, y_proba=y_proba, sample_weight=sample_weight)
    assert 0 <= score <= 1

def test_d2_log_loss_score_exception_for_both_y_pred_and_y_proba():
    y_true = [0, 1, 0, 1]
    y_proba = [[0.9, 0.1], [0.2, 0.8], [0.8, 0.2], [0.3, 0.7]]
    with pytest.raises(ValueError, match="Cannot use both `y_pred` and `y_proba`. `y_pred` is deprecated, use `y_proba` instead."):
        d2_log_loss_score(y_true, y_proba=y_proba, y_pred=y_proba)