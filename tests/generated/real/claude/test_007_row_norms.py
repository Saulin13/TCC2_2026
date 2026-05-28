import pytest
import numpy as np
from scipy import sparse
from sklearn.utils.extmath import row_norms


def test_row_norms_dense_2d_array():
    X = np.array([[3.0, 4.0], [5.0, 12.0], [8.0, 15.0]])
    result = row_norms(X, squared=False)
    expected = np.array([5.0, 13.0, 17.0])
    np.testing.assert_array_almost_equal(result, expected)


def test_row_norms_dense_2d_array_squared():
    X = np.array([[3.0, 4.0], [5.0, 12.0], [8.0, 15.0]])
    result = row_norms(X, squared=True)
    expected = np.array([25.0, 169.0, 289.0])
    np.testing.assert_array_almost_equal(result, expected)


def test_row_norms_single_row():
    X = np.array([[3.0, 4.0]])
    result = row_norms(X, squared=False)
    expected = np.array([5.0])
    np.testing.assert_array_almost_equal(result, expected)


def test_row_norms_single_column():
    X = np.array([[3.0], [4.0], [5.0]])
    result = row_norms(X, squared=False)
    expected = np.array([3.0, 4.0, 5.0])
    np.testing.assert_array_almost_equal(result, expected)


def test_row_norms_zeros():
    X = np.array([[0.0, 0.0], [0.0, 0.0]])
    result = row_norms(X, squared=False)
    expected = np.array([0.0, 0.0])
    np.testing.assert_array_almost_equal(result, expected)


def test_row_norms_negative_values():
    X = np.array([[-3.0, 4.0], [-5.0, -12.0]])
    result = row_norms(X, squared=False)
    expected = np.array([5.0, 13.0])
    np.testing.assert_array_almost_equal(result, expected)


def test_row_norms_sparse_csr():
    X = sparse.csr_matrix([[3.0, 4.0], [5.0, 12.0], [0.0, 0.0]])
    result = row_norms(X, squared=False)
    expected = np.array([5.0, 13.0, 0.0])
    np.testing.assert_array_almost_equal(result, expected)


def test_row_norms_sparse_csr_squared():
    X = sparse.csr_matrix([[3.0, 4.0], [5.0, 12.0]])
    result = row_norms(X, squared=True)
    expected = np.array([25.0, 169.0])
    np.testing.assert_array_almost_equal(result, expected)


def test_row_norms_sparse_coo():
    X = sparse.coo_matrix([[3.0, 4.0], [5.0, 12.0]])
    result = row_norms(X, squared=False)
    expected = np.array([5.0, 13.0])
    np.testing.assert_array_almost_equal(result, expected)


def test_row_norms_sparse_csc():
    X = sparse.csc_matrix([[3.0, 4.0], [5.0, 12.0]])
    result = row_norms(X, squared=False)
    expected = np.array([5.0, 13.0])
    np.testing.assert_array_almost_equal(result, expected)


def test_row_norms_large_values():
    X = np.array([[1e6, 1e6], [2e6, 2e6]])
    result = row_norms(X, squared=True)
    expected = np.array([2e12, 8e12])
    np.testing.assert_array_almost_equal(result, expected)


def test_row_norms_small_values():
    X = np.array([[1e-6, 1e-6], [2e-6, 2e-6]])
    result = row_norms(X, squared=False)
    expected = np.array([np.sqrt(2) * 1e-6, np.sqrt(2) * 2e-6])
    np.testing.assert_array_almost_equal(result, expected)


def test_row_norms_mixed_sparse_dense():
    X_dense = np.array([[3.0, 4.0], [5.0, 12.0]])
    X_sparse = sparse.csr_matrix(X_dense)
    result_dense = row_norms(X_dense, squared=False)
    result_sparse = row_norms(X_sparse, squared=False)
    np.testing.assert_array_almost_equal(result_dense, result_sparse)


def test_row_norms_wide_matrix():
    X = np.array([[1.0, 2.0, 3.0, 4.0, 5.0]])
    result = row_norms(X, squared=False)
    expected = np.array([np.sqrt(55.0)])
    np.testing.assert_array_almost_equal(result, expected)


def test_row_norms_tall_matrix():
    X = np.array([[1.0], [2.0], [3.0], [4.0], [5.0]])
    result = row_norms(X, squared=False)
    expected = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    np.testing.assert_array_almost_equal(result, expected)