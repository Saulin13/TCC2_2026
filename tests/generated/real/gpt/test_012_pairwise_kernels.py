import pytest
import numpy as np
from sklearn.metrics.pairwise import pairwise_kernels

def test_pairwise_kernels_linear():
    X = [[0, 0, 0], [1, 1, 1]]
    Y = [[1, 0, 0], [1, 1, 0]]
    expected = np.array([[0., 0.], [1., 2.]])
    result = pairwise_kernels(X, Y, metric='linear')
    assert np.allclose(result, expected)

def test_pairwise_kernels_rbf():
    X = [[0, 0], [1, 1]]
    Y = [[1, 0], [0, 1]]
    expected = np.array([[0.36787944, 0.36787944], [0.60653066, 0.60653066]])
    result = pairwise_kernels(X, Y, metric='rbf', gamma=1.0)
    assert np.allclose(result, expected)

def test_pairwise_kernels_precomputed():
    X = np.array([[1, 0], [0, 1]])
    result = pairwise_kernels(X, metric='precomputed')
    assert np.array_equal(result, X)

def test_pairwise_kernels_invalid_metric():
    X = [[0, 0], [1, 1]]
    with pytest.raises(ValueError, match="Unknown kernel"):
        pairwise_kernels(X, metric='invalid_metric')

def test_pairwise_kernels_empty_input():
    X = np.array([]).reshape(0, 3)
    Y = np.array([]).reshape(0, 3)
    result = pairwise_kernels(X, Y, metric='linear')
    expected = np.array([]).reshape(0, 0)
    assert np.array_equal(result, expected)

def test_pairwise_kernels_callable_metric():
    def custom_metric(x, y):
        return np.dot(x, y) + 1

    X = [[0, 0], [1, 1]]
    Y = [[1, 0], [0, 1]]
    expected = np.array([[1., 1.], [2., 2.]])
    result = pairwise_kernels(X, Y, metric=custom_metric)
    assert np.allclose(result, expected)