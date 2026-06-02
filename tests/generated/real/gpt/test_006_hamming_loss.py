import pytest
import numpy as np
from sklearn.metrics._classification import hamming_loss

def test_hamming_loss_basic():
    y_true = [1, 2, 3, 4]
    y_pred = [2, 2, 3, 4]
    assert hamming_loss(y_true, y_pred) == 0.25

def test_hamming_loss_perfect_match():
    y_true = [1, 2, 3, 4]
    y_pred = [1, 2, 3, 4]
    assert hamming_loss(y_true, y_pred) == 0.0

def test_hamming_loss_all_wrong():
    y_true = [1, 1, 1, 1]
    y_pred = [0, 0, 0, 0]
    assert hamming_loss(y_true, y_pred) == 1.0

def test_hamming_loss_multilabel():
    y_true = np.array([[0, 1], [1, 1]])
    y_pred = np.zeros((2, 2))
    assert hamming_loss(y_true, y_pred) == 0.75

def test_hamming_loss_with_sample_weight():
    y_true = [1, 2, 3, 4]
    y_pred = [2, 2, 3, 4]
    sample_weight = [1, 1, 1, 0]
    assert hamming_loss(y_true, y_pred, sample_weight=sample_weight) == 0.3333333333333333

def test_hamming_loss_empty_input():
    y_true = []
    y_pred = []
    assert hamming_loss(y_true, y_pred) == 0.0

def test_hamming_loss_mismatched_lengths():
    y_true = [1, 2, 3]
    y_pred = [1, 2]
    with pytest.raises(ValueError):
        hamming_loss(y_true, y_pred)

def test_hamming_loss_invalid_type():
    y_true = [1, 2, 3]
    y_pred = "invalid"
    with pytest.raises(ValueError):
        hamming_loss(y_true, y_pred)