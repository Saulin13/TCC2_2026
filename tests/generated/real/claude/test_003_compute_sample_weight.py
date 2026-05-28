import pytest
import numpy as np
from scipy import sparse
from sklearn.utils.class_weight import compute_sample_weight


def test_compute_sample_weight_balanced_basic():
    y = [1, 1, 1, 1, 0, 0]
    weights = compute_sample_weight(class_weight="balanced", y=y)
    expected = np.array([0.75, 0.75, 0.75, 0.75, 1.5, 1.5])
    np.testing.assert_array_almost_equal(weights, expected)


def test_compute_sample_weight_dict_basic():
    y = [0, 0, 1, 1, 1]
    class_weight = {0: 2.0, 1: 1.0}
    weights = compute_sample_weight(class_weight=class_weight, y=y)
    expected = np.array([2.0, 2.0, 1.0, 1.0, 1.0])
    np.testing.assert_array_equal(weights, expected)


def test_compute_sample_weight_none():
    y = [0, 1, 2, 0, 1]
    weights = compute_sample_weight(class_weight=None, y=y)
    expected = np.ones(5)
    np.testing.assert_array_equal(weights, expected)


def test_compute_sample_weight_balanced_equal_classes():
    y = [0, 1, 2, 0, 1, 2]
    weights = compute_sample_weight(class_weight="balanced", y=y)
    expected = np.ones(6)
    np.testing.assert_array_almost_equal(weights, expected)


def test_compute_sample_weight_balanced_with_indices():
    y = [0, 0, 0, 1, 1, 1, 2, 2, 2]
    indices = [0, 1, 3, 4, 6, 7]
    weights = compute_sample_weight(class_weight="balanced", y=y, indices=indices)
    assert len(weights) == len(y)
    assert weights[2] == 0.0
    assert weights[5] == 0.0
    assert weights[8] == 0.0


def test_compute_sample_weight_multioutput_balanced():
    y = np.array([[0, 1], [0, 1], [1, 0], [1, 0]])
    weights = compute_sample_weight(class_weight="balanced", y=y)
    assert len(weights) == 4
    assert all(weights > 0)


def test_compute_sample_weight_multioutput_list_of_dicts():
    y = np.array([[0, 1], [0, 1], [1, 0], [1, 0]])
    class_weight = [{0: 1.0, 1: 2.0}, {0: 2.0, 1: 1.0}]
    weights = compute_sample_weight(class_weight=class_weight, y=y)
    expected = np.array([2.0, 2.0, 4.0, 4.0])
    np.testing.assert_array_equal(weights, expected)


def test_compute_sample_weight_sparse_matrix():
    y = sparse.csr_matrix([[0], [1], [1], [0]])
    weights = compute_sample_weight(class_weight="balanced", y=y)
    expected = np.array([1.0, 1.0, 1.0, 1.0])
    np.testing.assert_array_almost_equal(weights, expected)


def test_compute_sample_weight_single_class():
    y = [1, 1, 1, 1]
    weights = compute_sample_weight(class_weight="balanced", y=y)
    expected = np.ones(4)
    np.testing.assert_array_equal(weights, expected)


def test_compute_sample_weight_dict_with_three_classes():
    y = [0, 1, 2, 0, 1, 2, 2]
    class_weight = {0: 1.0, 1: 2.0, 2: 3.0}
    weights = compute_sample_weight(class_weight=class_weight, y=y)
    expected = np.array([1.0, 2.0, 3.0, 1.0, 2.0, 3.0, 3.0])
    np.testing.assert_array_equal(weights, expected)


def test_compute_sample_weight_1d_array():
    y = np.array([0, 1, 0, 1, 1])
    weights = compute_sample_weight(class_weight="balanced", y=y)
    assert len(weights) == 5
    assert weights[0] == weights[2]
    assert weights[1] == weights[3] == weights[4]


def test_compute_sample_weight_indices_with_repetition():
    y = [0, 0, 1, 1, 2, 2]
    indices = [0, 0, 2, 2, 4, 4]
    weights = compute_sample_weight(class_weight="balanced", y=y, indices=indices)
    assert len(weights) == 6


def test_compute_sample_weight_exception_indices_with_dict():
    y = [0, 1, 0, 1]
    class_weight = {0: 1.0, 1: 2.0}
    indices = [0, 1]
    with pytest.raises(ValueError, match="The only valid class_weight for subsampling is 'balanced'"):
        compute_sample_weight(class_weight=class_weight, y=y, indices=indices)


def test_compute_sample_weight_exception_multioutput_with_dict():
    y = np.array([[0, 1], [1, 0], [0, 1]])
    class_weight = {0: 1.0, 1: 2.0}
    with pytest.raises(ValueError, match="For multi-output, class_weight should be a list of dicts"):
        compute_sample_weight(class_weight=class_weight, y=y)


def test_compute_sample_weight_exception_multioutput_with_none():
    y = np.array([[0, 1], [1, 0], [0, 1]])
    with pytest.raises(ValueError, match="For multi-output, class_weight should be a list of dicts"):
        compute_sample_weight(class_weight=None, y=y)


def test_compute_sample_weight_exception_multioutput_wrong_length():
    y = np.array([[0, 1], [1, 0], [0, 1]])
    class_weight = [{0: 1.0, 1: 2.0}]
    with pytest.raises(ValueError, match="number of elements in class_weight should match number of outputs"):
        compute_sample_weight(class_weight=class_weight, y=y)


def test_compute_sample_weight_balanced_imbalanced():
    y = [0, 1, 1, 1, 1, 1]
    weights = compute_sample_weight(class_weight="balanced", y=y)
    assert weights[0] > weights[1]
    assert np.isclose(weights[0], 3.0)
    assert np.isclose(weights[1], 0.6)


def test_compute_sample_weight_empty_dict():
    y = [0, 1, 0, 1]
    class_weight = {}
    weights = compute_sample_weight(class_weight=class_weight, y=y)
    assert len(weights) == 4