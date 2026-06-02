import pytest
import numpy as np
from sklearn.metrics._classification import hamming_loss
from scipy.sparse import csr_matrix


def test_hamming_loss_binary_perfect_match():
    y_true = [0, 1, 0, 1]
    y_pred = [0, 1, 0, 1]
    assert hamming_loss(y_true, y_pred) == 0.0


def test_hamming_loss_binary_all_wrong():
    y_true = [0, 0, 0, 0]
    y_pred = [1, 1, 1, 1]
    assert hamming_loss(y_true, y_pred) == 1.0


def test_hamming_loss_binary_partial():
    y_true = [1, 2, 3, 4]
    y_pred = [2, 2, 3, 4]
    assert hamming_loss(y_true, y_pred) == 0.25


def test_hamming_loss_multiclass():
    y_true = [0, 1, 2, 3, 4]
    y_pred = [0, 2, 2, 3, 1]
    assert hamming_loss(y_true, y_pred) == 0.4


def test_hamming_loss_multiclass_strings():
    y_true = ['cat', 'dog', 'bird', 'fish']
    y_pred = ['cat', 'cat', 'bird', 'fish']
    assert hamming_loss(y_true, y_pred) == 0.25


def test_hamming_loss_multilabel_binary_indicators():
    y_true = np.array([[0, 1], [1, 1]])
    y_pred = np.zeros((2, 2))
    assert hamming_loss(y_true, y_pred) == 0.75


def test_hamming_loss_multilabel_all_correct():
    y_true = np.array([[1, 0, 1], [0, 1, 0]])
    y_pred = np.array([[1, 0, 1], [0, 1, 0]])
    assert hamming_loss(y_true, y_pred) == 0.0


def test_hamming_loss_multilabel_partial():
    y_true = np.array([[1, 0, 1], [0, 1, 0]])
    y_pred = np.array([[1, 1, 1], [0, 1, 0]])
    expected = 1.0 / 6.0
    assert abs(hamming_loss(y_true, y_pred) - expected) < 1e-10


def test_hamming_loss_with_sample_weight():
    y_true = [1, 2, 3, 4]
    y_pred = [2, 2, 3, 4]
    sample_weight = [1, 1, 1, 1]
    assert hamming_loss(y_true, y_pred, sample_weight=sample_weight) == 0.25


def test_hamming_loss_with_unequal_sample_weight():
    y_true = [1, 2, 3, 4]
    y_pred = [2, 2, 3, 4]
    sample_weight = [2, 1, 1, 1]
    expected = 2.0 / 5.0
    assert abs(hamming_loss(y_true, y_pred, sample_weight=sample_weight) - expected) < 1e-10


def test_hamming_loss_numpy_arrays():
    y_true = np.array([0, 1, 2, 3])
    y_pred = np.array([0, 1, 1, 3])
    assert hamming_loss(y_true, y_pred) == 0.25


def test_hamming_loss_single_sample():
    y_true = [1]
    y_pred = [1]
    assert hamming_loss(y_true, y_pred) == 0.0


def test_hamming_loss_single_sample_wrong():
    y_true = [1]
    y_pred = [0]
    assert hamming_loss(y_true, y_pred) == 1.0


def test_hamming_loss_multilabel_sparse():
    y_true = csr_matrix(np.array([[1, 0, 1], [0, 1, 0]]))
    y_pred = csr_matrix(np.array([[1, 1, 1], [0, 1, 0]]))
    expected = 1.0 / 6.0
    assert abs(hamming_loss(y_true, y_pred) - expected) < 1e-10


def test_hamming_loss_multilabel_with_sample_weight():
    y_true = np.array([[1, 0, 1], [0, 1, 0]])
    y_pred = np.array([[1, 1, 1], [0, 1, 0]])
    sample_weight = [1, 1]
    expected = 1.0 / 6.0
    assert abs(hamming_loss(y_true, y_pred, sample_weight=sample_weight) - expected) < 1e-10


def test_hamming_loss_empty_arrays():
    with pytest.raises((ValueError, IndexError)):
        y_true = []
        y_pred = []
        hamming_loss(y_true, y_pred)


def test_hamming_loss_mismatched_lengths():
    with pytest.raises(ValueError):
        y_true = [1, 2, 3]
        y_pred = [1, 2]
        hamming_loss(y_true, y_pred)


def test_hamming_loss_multilabel_mismatched_shapes():
    with pytest.raises(ValueError):
        y_true = np.array([[1, 0, 1], [0, 1, 0]])
        y_pred = np.array([[1, 1], [0, 1]])
        hamming_loss(y_true, y_pred)