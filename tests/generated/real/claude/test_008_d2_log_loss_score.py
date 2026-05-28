import pytest
import numpy as np
import warnings
from sklearn.metrics._classification import d2_log_loss_score
from sklearn.exceptions import UndefinedMetricWarning


def test_d2_log_loss_score_perfect_prediction():
    """Test D^2 score with perfect predictions (should be 1.0)."""
    y_true = np.array([0, 1, 0, 1])
    y_proba = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 0.0], [0.0, 1.0]])
    score = d2_log_loss_score(y_true, y_proba)
    assert np.isclose(score, 1.0, atol=1e-10)


def test_d2_log_loss_score_baseline_prediction():
    """Test D^2 score with baseline predictions (should be 0.0)."""
    y_true = np.array([0, 1, 0, 1])
    # Predict class proportions (0.5, 0.5)
    y_proba = np.array([[0.5, 0.5], [0.5, 0.5], [0.5, 0.5], [0.5, 0.5]])
    score = d2_log_loss_score(y_true, y_proba)
    assert np.isclose(score, 0.0, atol=1e-10)


def test_d2_log_loss_score_good_prediction():
    """Test D^2 score with good but not perfect predictions."""
    y_true = np.array([0, 1, 0, 1])
    y_proba = np.array([[0.9, 0.1], [0.1, 0.9], [0.8, 0.2], [0.2, 0.8]])
    score = d2_log_loss_score(y_true, y_proba)
    assert 0.0 < score < 1.0


def test_d2_log_loss_score_poor_prediction():
    """Test D^2 score with poor predictions (can be negative)."""
    y_true = np.array([0, 1, 0, 1])
    # Predictions worse than baseline
    y_proba = np.array([[0.1, 0.9], [0.9, 0.1], [0.1, 0.9], [0.9, 0.1]])
    score = d2_log_loss_score(y_true, y_proba)
    assert score < 0.0


def test_d2_log_loss_score_binary_1d_proba():
    """Test D^2 score with 1D probability array for binary classification."""
    y_true = np.array([0, 1, 0, 1])
    y_proba = np.array([0.1, 0.9, 0.2, 0.8])  # Probabilities of positive class
    score = d2_log_loss_score(y_true, y_proba)
    assert 0.0 < score < 1.0


def test_d2_log_loss_score_multiclass():
    """Test D^2 score with multiclass classification."""
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
    """Test D^2 score with sample weights."""
    y_true = np.array([0, 1, 0, 1])
    y_proba = np.array([[0.9, 0.1], [0.1, 0.9], [0.8, 0.2], [0.2, 0.8]])
    sample_weight = np.array([1.0, 1.0, 2.0, 2.0])
    score = d2_log_loss_score(y_true, y_proba, sample_weight=sample_weight)
    assert 0.0 < score < 1.0


def test_d2_log_loss_score_with_labels():
    """Test D^2 score with explicit labels."""
    y_true = np.array(['cat', 'dog', 'cat', 'dog'])
    y_proba = np.array([[0.9, 0.1], [0.1, 0.9], [0.8, 0.2], [0.2, 0.8]])
    labels = ['cat', 'dog']
    score = d2_log_loss_score(y_true, y_proba, labels=labels)
    assert 0.0 < score < 1.0


def test_d2_log_loss_score_single_sample_warning():
    """Test that a warning is raised and NaN is returned for single sample."""
    y_true = np.array([0])
    y_proba = np.array([[0.9, 0.1]])
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        score = d2_log_loss_score(y_true, y_proba)
        assert len(w) == 1
        assert issubclass(w[0].category, UndefinedMetricWarning)
        assert "less than two samples" in str(w[0].message)
    
    assert np.isnan(score)


def test_d2_log_loss_score_deprecated_y_pred_warning():
    """Test that using y_pred raises a deprecation warning."""
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
    """Test that using both y_pred and y_proba raises ValueError."""
    y_true = np.array([0, 1, 0, 1])
    y_proba = np.array([[0.9, 0.1], [0.1, 0.9], [0.8, 0.2], [0.2, 0.8]])
    y_pred = np.array([[0.9, 0.1], [0.1, 0.9], [0.8, 0.2], [0.2, 0.8]])
    
    with pytest.raises(ValueError, match="Cannot use both `y_pred` and `y_proba`"):
        d2_log_loss_score(y_true, y_proba=y_proba, y_pred=y_pred)


def test_d2_log_loss_score_inconsistent_length_raises():
    """Test that inconsistent lengths raise an error."""
    y_true = np.array([0, 1, 0, 1])
    y_proba = np.array([[0.9, 0.1], [0.1, 0.9]])  # Only 2 samples
    
    with pytest.raises(ValueError):
        d2_log_loss_score(y_true, y_proba)


def test_d2_log_loss_score_imbalanced_classes():
    """Test D^2 score with imbalanced classes."""
    y_true = np.array([0, 0, 0, 1])
    y_proba = np.array([[0.9, 0.1], [0.8, 0.2], [0.85, 0.15], [0.1, 0.9]])
    score = d2_log_loss_score(y_true, y_proba)
    assert 0.0 < score < 1.0