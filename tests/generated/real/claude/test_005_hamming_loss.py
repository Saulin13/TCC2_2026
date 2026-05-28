import pytest
import numpy as np
from sklearn.metrics._classification import hamming_loss
from scipy.sparse import csr_matrix


def test_hamming_loss_binary_perfect_prediction():
    y_true = [0, 1, 0, 1]
    y_pred = [0, 1, 0, 1]
    assert hamming_loss(y_true, y_pred) == 0.0


def test_hamming_loss_binary_all_wrong():
    y_true = [0, 0, 0, 0]
    y_pred = [1, 1, 1, 1]
    assert hamming_loss(y_true, y_pred) == 1.0


def test_hamming_loss_binary_partial_mismatch():
    y_true = [0, 1, 0, 1]
    y_pred = [1, 1, 0, 1]
    assert hamming_loss(y_true, y_pred) == 0.25


def test_hamming_loss_multiclass():
    y_true = [2, 2, 3, 4]
    y_pred = [1, 2, 3, 4]
    assert hamming_loss(y_true, y_pred) == 0.25


def test_hamming_loss_multiclass_all_correct():
    y_true = [1, 2, 3, 4, 5]
    y_pred = [1, 2, 3, 4, 5]
    assert hamming_loss(y_true, y_pred) == 0.0


def test_hamming_loss_multiclass_all_wrong():
    y_true = [1, 2, 3]
    y_pred = [4, 5, 6]
    assert hamming_loss(y_true, y_pred) == 1.0


def test_hamming_loss_multilabel_binary_indicators():
    y_true = np.array([[0, 1], [1, 1]])
    y_pred = np.zeros((2, 2))
    assert hamming_loss(y_true, y_pred) == 0.75


def test_hamming_loss_multilabel_perfect():
    y_true = np.array([[1, 0, 1], [0, 1, 0]])
    y_pred = np.array([[1, 0, 1], [0, 1, 0]])
    assert hamming_loss(y_true, y_pred) == 0.0


def test_hamming_loss_multilabel_partial():
    y_true = np.array([[1, 0, 1], [0, 1, 0]])
    y_pred = np.array([[1, 1, 1], [0, 1, 0]])
    expected = 1.0 / 6.0
    assert abs(hamming_loss(y_true, y_pred) - expected) < 1e-10


def test_hamming_loss_with_sample_weight():
    y_true = [0, 1, 0, 1]
    y_pred = [1, 1, 0, 0]
    sample_weight = [1, 1, 1, 1]
    assert hamming_loss(y_true, y_pred, sample_weight=sample_weight) == 0.5


def test_hamming_loss_with_unequal_sample_weight():
    y_true = [0, 1, 0, 1]
    y_pred = [1, 1, 0, 0]
    sample_weight = [1, 2, 1, 2]
    expected = (1 + 2) / (1 + 2 + 1 + 2)
    assert abs(hamming_loss(y_true, y_pred, sample_weight=sample_weight) - expected) < 1e-10


def test_hamming_loss_numpy_arrays():
    y_true = np.array([1, 2, 3, 4])
    y_pred = np.array([1, 2, 4, 4])
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


def test_hamming_loss_multilabel_all_zeros():
    y_true = np.array([[0, 0, 0], [0, 0, 0]])
    y_pred = np.array([[0, 0, 0], [0, 0, 0]])
    assert hamming_loss(y_true, y_pred) == 0.0


def test_hamming_loss_multilabel_all_ones():
    y_true = np.array([[1, 1, 1], [1, 1, 1]])
    y_pred = np.array([[1, 1, 1], [1, 1, 1]])
    assert hamming_loss(y_true, y_pred) == 0.0


def test_hamming_loss_empty_raises():
    with pytest.raises((ValueError, IndexError)):
        hamming_loss([], [])


def test_hamming_loss_mismatched_length():
    y_true = [1, 2, 3]
    y_pred = [1, 2]
    with pytest.raises(ValueError):
        hamming_loss(y_true, y_pred)


def test_hamming_loss_multilabel_mismatched_shape():
    y_true = np.array([[1, 0, 1], [0, 1, 0]])
    y_pred = np.array([[1, 0], [0, 1]])
    with pytest.raises(ValueError):
        hamming_loss(y_true, y_pred)