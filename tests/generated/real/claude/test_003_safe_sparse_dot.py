import pytest
import numpy as np
from scipy import sparse
from sklearn.utils.extmath import safe_sparse_dot


def test_safe_sparse_dot_dense_dense():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])
    result = safe_sparse_dot(a, b)
    expected = np.array([[19, 22], [43, 50]])
    np.testing.assert_array_equal(result, expected)


def test_safe_sparse_dot_sparse_sparse_csr():
    a = sparse.csr_matrix([[1, 2], [3, 4], [5, 6]])
    b = sparse.csr_matrix([[1, 2, 3], [4, 5, 6]])
    result = safe_sparse_dot(a, b)
    expected = np.array([[9, 12, 15], [19, 26, 33], [29, 40, 51]])
    assert sparse.issparse(result)
    np.testing.assert_array_equal(result.toarray(), expected)


def test_safe_sparse_dot_sparse_sparse_dense_output():
    a = sparse.csr_matrix([[1, 2], [3, 4]])
    b = sparse.csr_matrix([[5, 6], [7, 8]])
    result = safe_sparse_dot(a, b, dense_output=True)
    expected = np.array([[19, 22], [43, 50]])
    assert isinstance(result, np.ndarray)
    np.testing.assert_array_equal(result, expected)


def test_safe_sparse_dot_sparse_dense():
    a = sparse.csr_matrix([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])
    result = safe_sparse_dot(a, b)
    expected = np.array([[19, 22], [43, 50]])
    np.testing.assert_array_equal(result, expected)


def test_safe_sparse_dot_dense_sparse():
    a = np.array([[1, 2], [3, 4]])
    b = sparse.csr_matrix([[5, 6], [7, 8]])
    result = safe_sparse_dot(a, b)
    expected = np.array([[19, 22], [43, 50]])
    np.testing.assert_array_equal(result, expected)


def test_safe_sparse_dot_sparse_transpose():
    X = sparse.csr_matrix([[1, 2], [3, 4], [5, 6]])
    result = safe_sparse_dot(X, X.T)
    expected = np.array([[5, 11, 17], [11, 25, 39], [17, 39, 61]])
    np.testing.assert_array_equal(result.toarray(), expected)


def test_safe_sparse_dot_3d_dense_sparse():
    a = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
    b = sparse.csr_matrix([[1, 2, 3], [4, 5, 6]])
    result = safe_sparse_dot(a, b)
    expected_0 = np.array([[9, 12, 15], [19, 26, 33]])
    expected_1 = np.array([[29, 40, 51], [39, 54, 69]])
    expected = np.array([expected_0, expected_1])
    np.testing.assert_array_equal(result, expected)


def test_safe_sparse_dot_sparse_3d_dense():
    a = sparse.csr_matrix([[1, 2], [3, 4]])
    b = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
    result = safe_sparse_dot(a, b)
    expected = np.array([[7, 10], [15, 22]])
    np.testing.assert_array_equal(result, expected)


def test_safe_sparse_dot_3d_dense_dense():
    a = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
    b = np.array([[1, 2], [3, 4]])
    result = safe_sparse_dot(a, b)
    expected_0 = np.array([[7, 10], [15, 22]])
    expected_1 = np.array([[23, 34], [31, 46]])
    expected = np.array([expected_0, expected_1])
    np.testing.assert_array_equal(result, expected)


def test_safe_sparse_dot_csc_format():
    a = sparse.csc_matrix([[1, 2], [3, 4]])
    b = sparse.csc_matrix([[5, 6], [7, 8]])
    result = safe_sparse_dot(a, b, dense_output=True)
    expected = np.array([[19, 22], [43, 50]])
    assert isinstance(result, np.ndarray)
    np.testing.assert_array_equal(result, expected)


def test_safe_sparse_dot_float32():
    a = sparse.csr_matrix([[1.0, 2.0], [3.0, 4.0]], dtype=np.float32)
    b = sparse.csr_matrix([[5.0, 6.0], [7.0, 8.0]], dtype=np.float32)
    result = safe_sparse_dot(a, b, dense_output=True)
    expected = np.array([[19.0, 22.0], [43.0, 50.0]], dtype=np.float32)
    assert isinstance(result, np.ndarray)
    np.testing.assert_array_almost_equal(result, expected)


def test_safe_sparse_dot_empty_matrix():
    a = np.array([[]])
    b = np.array([[]])
    with pytest.raises((ValueError, IndexError)):
        safe_sparse_dot(a, b)


def test_safe_sparse_dot_incompatible_shapes():
    a = np.array([[1, 2, 3]])
    b = np.array([[1, 2]])
    with pytest.raises(ValueError):
        safe_sparse_dot(a, b)


def test_safe_sparse_dot_vector_matrix():
    a = np.array([1, 2, 3])
    b = np.array([[1], [2], [3]])
    result = safe_sparse_dot(a, b)
    expected = np.array([14])
    np.testing.assert_array_equal(result, expected)


def test_safe_sparse_dot_zeros():
    a = sparse.csr_matrix([[0, 0], [0, 0]])
    b = sparse.csr_matrix([[1, 2], [3, 4]])
    result = safe_sparse_dot(a, b)
    expected = np.array([[0, 0], [0, 0]])
    np.testing.assert_array_equal(result.toarray(), expected)