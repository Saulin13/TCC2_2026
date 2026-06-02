import pytest
import numpy as np
import warnings
from sklearn.metrics._classification import d2_log_loss_score
from sklearn.exceptions import UndefinedMetricWarning


def test_d2_log_loss_score_perfect_prediction():
    y_true = np.array([0, 1, 0, 1])
    y_proba = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 0.0], [0.0, 1.0]])
    score = d2_log_loss_score(y_true, y_proba)
    assert score == pytest.approx(1.0, abs=1e-10)


def test_d2_log_loss_score_baseline_prediction():
    y_true = np.array([0, 1, 0, 1])
    y_proba = np.array([[0.5, 0.5], [0.5, 0.5], [0.5, 0.5], [0.5, 0.5]])
    score = d2_log_loss_score(y_true, y_proba)
    assert score == pytest.approx(0.0, abs=1e-10)


def test_d2_log_loss_score_binary_with_probabilities():
    y_true = np.array([0, 0, 1, 1])
    y_proba = np.array([[0.9, 0.1], [0.8, 0.2], [0.2, 0.8], [0.1, 0.9]])
    score = d2_log_loss_score(y_true, y_proba)
    assert 0.0 < score < 1.0


def test_d2_log_loss_score_binary_single_column():
    y_true = np.array([0, 0, 1, 1])
    y_proba = np.array([0.1, 0.2, 0.8, 0.9])
    score = d2_log_loss_score(y_true, y_proba)
    assert 0.0 < score < 1.0


def test_d2_log_loss_score_multiclass():
    y_true = np.array([0, 1, 2, 0, 1, 2])
    y_proba = np.array([
        [0.8, 0.1, 0.1],
        [0.1, 0.8, 0.1],
        [0.1, 0.1, 0.8],
        [0.7, 0.2, 0.1],
        [0.2, 0.7, 0.1],
        [0.1, 0.2, 0.7]
    ])
    score = d2_log_loss_score(y_true, y_proba)
    assert 0.0 < score < 1.0


def test_d2_log_loss_score_with_sample_weights():
    y_true = np.array([0, 1, 0, 1])
    y_proba = np.array([[0.9, 0.1], [0.1, 0.9], [0.8, 0.2], [0.2, 0.8]])
    sample_weight = np.array([1.0, 1.0, 2.0, 2.0])
    score = d2_log_loss_score(y_true, y_proba, sample_weight=sample_weight)
    assert 0.0 < score < 1.0


def test_d2_log_loss_score_with_labels():
    y_true = np.array(['cat', 'dog', 'cat', 'dog'])
    y_proba = np.array([[0.9, 0.1], [0.1, 0.9], [0.8, 0.2], [0.2, 0.8]])
    labels = ['cat', 'dog']
    score = d2_log_loss_score(y_true, y_proba, labels=labels)
    assert 0.0 < score < 1.0


def test_d2_log_loss_score_negative_score():
    y_true = np.array([0, 1, 0, 1])
    y_proba = np.array([[0.1, 0.9], [0.9, 0.1], [0.1, 0.9], [0.9, 0.1]])
    score = d2_log_loss_score(y_true, y_proba)
    assert score < 0.0


def test_d2_log_loss_score_single_sample_returns_nan():
    y_true = np.array([0])
    y_proba = np.array([[0.9, 0.1]])
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        score = d2_log_loss_score(y_true, y_proba)
        assert len(w) == 1
        assert issubclass(w[0].category, UndefinedMetricWarning)
        assert "less than two samples" in str(w[0].message)
    assert np.isnan(score)


def test_d2_log_loss_score_deprecated_y_pred_parameter():
    y_true = np.array([0, 1, 0, 1])
    y_pred = np.array([[0.9, 0.1], [0.1, 0.9], [0.8, 0.2], [0.2, 0.8]])
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        score = d2_log_loss_score(y_true, y_pred=y_pred)
        assert len(w) == 1
        assert issubclass(w[0].category, FutureWarning)
        assert "y_pred` was renamed to `y_proba" in str(w[0].message)
    assert 0.0 < score < 1.0


def test_d2_log_loss_score_both_y_pred_and_y_proba_raises():
    y_true = np.array([0, 1, 0, 1])
    y_proba = np.array([[0.9, 0.1], [0.1, 0.9], [0.8, 0.2], [0.2, 0.8]])
    y_pred = np.array([[0.9, 0.1], [0.1, 0.9], [0.8, 0.2], [0.2, 0.8]])
    with pytest.raises(ValueError, match="Cannot use both `y_pred` and `y_proba`"):
        d2_log_loss_score(y_true, y_proba=y_proba, y_pred=y_pred)


def test_d2_log_loss_score_inconsistent_length_raises():
    y_true = np.array([0, 1, 0, 1])
    y_proba = np.array([[0.9, 0.1], [0.1, 0.9]])
    with pytest.raises(ValueError):
        d2_log_loss_score(y_true, y_proba)


def test_d2_log_loss_score_empty_arrays():
    y_true = np.array([])
    y_proba = np.array([]).reshape(0, 2)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        score = d2_log_loss_score(y_true, y_proba)
        assert len(w) == 1
        assert issubclass(w[0].category, UndefinedMetricWarning)
    assert np.isnan(score)