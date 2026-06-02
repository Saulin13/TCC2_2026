import pytest
import numpy as np
from sklearn.metrics.pairwise import pairwise_kernels
from sklearn.gaussian_process.kernels import RBF
from scipy.sparse import csr_matrix


def test_pairwise_kernels_linear_basic():
    X = np.array([[0, 0, 0], [1, 1, 1]])
    Y = np.array([[1, 0, 0], [1, 1, 0]])
    result = pairwise_kernels(X, Y, metric='linear')
    expected = np.array([[0., 0.], [1., 2.]])
    np.testing.assert_array_almost_equal(result, expected)


def test_pairwise_kernels_linear_self():
    X = np.array([[1, 2], [3, 4], [5, 6]])
    result = pairwise_kernels(X, metric='linear')
    expected = np.dot(X, X.T)
    np.testing.assert_array_almost_equal(result, expected)


def test_pairwise_kernels_rbf():
    X = np.array([[0, 0], [1, 1]])
    Y = np.array([[2, 2], [3, 3]])
    result = pairwise_kernels(X, Y, metric='rbf', gamma=1.0)
    assert result.shape == (2, 2)
    assert np.all(result >= 0)
    assert np.all(result <= 1)


def test_pairwise_kernels_polynomial():
    X = np.array([[1, 2], [3, 4]])
    Y = np.array([[5, 6], [7, 8]])
    result = pairwise_kernels(X, Y, metric='polynomial', degree=2, gamma=1, coef0=1)
    assert result.shape == (2, 2)
    expected_00 = (1 * 5 + 2 * 6 + 1) ** 2
    np.testing.assert_almost_equal(result[0, 0], expected_00)


def test_pairwise_kernels_sigmoid():
    X = np.array([[1, 2], [3, 4]])
    result = pairwise_kernels(X, metric='sigmoid', gamma=0.1, coef0=1)
    assert result.shape == (2, 2)
    assert np.all(np.isfinite(result))


def test_pairwise_kernels_cosine():
    X = np.array([[1, 0], [0, 1], [1, 1]])
    result = pairwise_kernels(X, metric='cosine')
    assert result.shape == (3, 3)
    np.testing.assert_almost_equal(result[0, 0], 1.0)
    np.testing.assert_almost_equal(result[1, 1], 1.0)
    np.testing.assert_almost_equal(result[0, 1], 0.0)


def test_pairwise_kernels_chi2():
    X = np.array([[1, 2, 3], [4, 5, 6]])
    Y = np.array([[7, 8, 9], [10, 11, 12]])
    result = pairwise_kernels(X, Y, metric='chi2')
    assert result.shape == (2, 2)
    assert np.all(np.isfinite(result))


def test_pairwise_kernels_additive_chi2():
    X = np.array([[1, 2, 3], [4, 5, 6]])
    result = pairwise_kernels(X, metric='additive_chi2')
    assert result.shape == (2, 2)
    assert np.all(np.isfinite(result))


def test_pairwise_kernels_laplacian():
    X = np.array([[1, 2], [3, 4]])
    Y = np.array([[5, 6], [7, 8]])
    result = pairwise_kernels(X, Y, metric='laplacian', gamma=0.5)
    assert result.shape == (2, 2)
    assert np.all(result >= 0)
    assert np.all(result <= 1)


def test_pairwise_kernels_precomputed():
    K = np.array([[1.0, 0.5], [0.5, 1.0]])
    result = pairwise_kernels(K, metric='precomputed')
    np.testing.assert_array_equal(result, K)


def test_pairwise_kernels_precomputed_with_Y():
    K = np.array([[1.0, 0.5], [0.5, 1.0]])
    Y = np.array([[1, 2], [3, 4]])
    result = pairwise_kernels(K, Y, metric='precomputed')
    np.testing.assert_array_equal(result, K)


def test_pairwise_kernels_callable():
    def custom_kernel(x, y):
        return np.sum(x * y)
    
    X = np.array([[1, 2], [3, 4]])
    Y = np.array([[5, 6], [7, 8]])
    result = pairwise_kernels(X, Y, metric=custom_kernel)
    assert result.shape == (2, 2)
    np.testing.assert_almost_equal(result[0, 0], 1*5 + 2*6)
    np.testing.assert_almost_equal(result[1, 1], 3*7 + 4*8)


def test_pairwise_kernels_gp_kernel():
    gp_kernel = RBF(length_scale=1.0)
    X = np.array([[0, 0], [1, 1], [2, 2]])
    result = pairwise_kernels(X, metric=gp_kernel)
    assert result.shape == (3, 3)
    np.testing.assert_almost_equal(result[0, 0], 1.0)
    assert np.all(result >= 0)
    assert np.all(result <= 1)


def test_pairwise_kernels_sparse():
    X = csr_matrix([[1, 0, 2], [0, 3, 0]])
    Y = csr_matrix([[0, 1, 0], [2, 0, 1]])
    result = pairwise_kernels(X, Y, metric='linear')
    assert result.shape == (2, 2)
    np.testing.assert_array_almost_equal(result, [[0., 2.], [0., 0.]])


def test_pairwise_kernels_filter_params():
    X = np.array([[1, 2], [3, 4]])
    result = pairwise_kernels(X, metric='linear', filter_params=True, invalid_param=123)
    assert result.shape == (2, 2)


def test_pairwise_kernels_n_jobs():
    X = np.random.rand(10, 5)
    result_single = pairwise_kernels(X, metric='rbf', n_jobs=1)
    result_multi = pairwise_kernels(X, metric='rbf', n_jobs=2)
    np.testing.assert_array_almost_equal(result_single, result_multi)


def test_pairwise_kernels_empty_array():
    X = np.array([]).reshape(0, 3)
    result = pairwise_kernels(X, metric='linear')
    assert result.shape == (0, 0)


def test_pairwise_kernels_single_sample():
    X = np.array([[1, 2, 3]])
    result = pairwise_kernels(X, metric='linear')
    expected = np.array([[14.]])
    np.testing.assert_array_almost_equal(result, expected)


def test_pairwise_kernels_invalid_metric():
    X = np.array([[1, 2], [3, 4]])
    with pytest.raises((ValueError, AttributeError)):
        pairwise_kernels(X, metric='invalid_metric')


def test_pairwise_kernels_mismatched_dimensions():
    X = np.array([[1, 2, 3], [4, 5, 6]])
    Y = np.array([[1, 2], [3, 4]])
    with pytest.raises(ValueError):
        pairwise_kernels(X, Y, metric='linear')