import pytest
import numpy as np
from scipy.sparse import csr_matrix, csc_matrix
from sklearn.utils.extmath import safe_sparse_dot

def test_safe_sparse_dot_dense():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])
    result = safe_sparse_dot(a, b)
    expected = np.array([[19, 22], [43, 50]])
    assert np.array_equal(result, expected)

def test_safe_sparse_dot_sparse():
    a = csr_matrix([[1, 2], [3, 4]])
    b = csr_matrix([[5, 6], [7, 8]])
    result = safe_sparse_dot(a, b)
    expected = csr_matrix([[19, 22], [43, 50]])
    assert (result != expected).nnz == 0

def test_safe_sparse_dot_sparse_dense_output():
    a = csr_matrix([[1, 2], [3, 4]])
    b = csr_matrix([[5, 6], [7, 8]])
    result = safe_sparse_dot(a, b, dense_output=True)
    expected = np.array([[19, 22], [43, 50]])
    assert np.array_equal(result, expected)

def test_safe_sparse_dot_mixed():
    a = np.array([[1, 2], [3, 4]])
    b = csr_matrix([[5, 6], [7, 8]])
    result = safe_sparse_dot(a, b)
    expected = np.array([[19, 22], [43, 50]])
    assert np.array_equal(result, expected)

def test_safe_sparse_dot_high_dim():
    a = np.random.rand(2, 3, 4)
    b = np.random.rand(4, 5)
    result = safe_sparse_dot(a, b)
    expected = np.tensordot(a, b, axes=[-1, 0])
    assert np.allclose(result, expected)

def test_safe_sparse_dot_sparse_high_dim():
    a = np.random.rand(2, 3, 4)
    b = csr_matrix(np.random.rand(4, 5))
    result = safe_sparse_dot(a, b)
    expected = np.tensordot(a, b.toarray(), axes=[-1, 0])
    assert np.allclose(result, expected)

def test_safe_sparse_dot_invalid_shapes():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6]])
    with pytest.raises(ValueError):
        safe_sparse_dot(a, b)

def test_safe_sparse_dot_empty():
    a = np.array([[]])
    b = np.array([[]])
    result = safe_sparse_dot(a, b)
    expected = np.array([[0]])
    assert np.array_equal(result, expected)

def test_safe_sparse_dot_empty_sparse():
    a = csr_matrix((0, 0))
    b = csr_matrix((0, 0))
    result = safe_sparse_dot(a, b)
    expected = csr_matrix((0, 0))
    assert (result != expected).nnz == 0