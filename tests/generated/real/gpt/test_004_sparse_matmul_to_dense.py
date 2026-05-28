import pytest
import numpy as np
from scipy.sparse import csc_matrix, csr_matrix
from sklearn.utils.sparsefuncs import sparse_matmul_to_dense

def test_sparse_matmul_to_dense_normal_case():
    A = csr_matrix([[1, 0], [0, 1]], dtype=np.float64)
    B = csr_matrix([[4, 1], [2, 2]], dtype=np.float64)
    expected = np.array([[4, 1], [2, 2]], dtype=np.float64)
    result = sparse_matmul_to_dense(A, B)
    assert np.array_equal(result, expected)

def test_sparse_matmul_to_dense_with_csc_format():
    A = csc_matrix([[1, 0], [0, 1]], dtype=np.float64)
    B = csc_matrix([[4, 1], [2, 2]], dtype=np.float64)
    expected = np.array([[4, 1], [2, 2]], dtype=np.float64)
    result = sparse_matmul_to_dense(A, B)
    assert np.array_equal(result, expected)

def test_sparse_matmul_to_dense_edge_case_empty_matrices():
    A = csr_matrix((0, 0), dtype=np.float64)
    B = csr_matrix((0, 0), dtype=np.float64)
    expected = np.array([], dtype=np.float64).reshape(0, 0)
    result = sparse_matmul_to_dense(A, B)
    assert np.array_equal(result, expected)

def test_sparse_matmul_to_dense_edge_case_single_element():
    A = csr_matrix([[2]], dtype=np.float64)
    B = csr_matrix([[3]], dtype=np.float64)
    expected = np.array([[6]], dtype=np.float64)
    result = sparse_matmul_to_dense(A, B)
    assert np.array_equal(result, expected)

def test_sparse_matmul_to_dense_with_out_parameter():
    A = csr_matrix([[1, 2], [3, 4]], dtype=np.float64)
    B = csr_matrix([[5, 6], [7, 8]], dtype=np.float64)
    out = np.empty((2, 2), dtype=np.float64)
    expected = np.array([[19, 22], [43, 50]], dtype=np.float64)
    sparse_matmul_to_dense(A, B, out=out)
    assert np.array_equal(out, expected)

def test_sparse_matmul_to_dense_invalid_shape():
    A = csr_matrix([[1, 2]], dtype=np.float64)
    B = csr_matrix([[3, 4]], dtype=np.float64)
    with pytest.raises(ValueError, match="Shapes must fulfil A.shape[1] == B.shape[0]"):
        sparse_matmul_to_dense(A, B)

def test_sparse_matmul_to_dense_invalid_dtype():
    A = csr_matrix([[1, 2]], dtype=np.int32)
    B = csr_matrix([[3, 4]], dtype=np.int32)
    with pytest.raises(ValueError, match="Dtype of A and B must be the same, either both float32 or float64"):
        sparse_matmul_to_dense(A, B)

def test_sparse_matmul_to_dense_invalid_out_shape():
    A = csr_matrix([[1, 2], [3, 4]], dtype=np.float64)
    B = csr_matrix([[5, 6], [7, 8]], dtype=np.float64)
    out = np.empty((3, 3), dtype=np.float64)
    with pytest.raises(ValueError, match="Shape of out must be"):
        sparse_matmul_to_dense(A, B, out=out)

def test_sparse_matmul_to_dense_invalid_out_dtype():
    A = csr_matrix([[1, 2], [3, 4]], dtype=np.float64)
    B = csr_matrix([[5, 6], [7, 8]], dtype=np.float64)
    out = np.empty((2, 2), dtype=np.float32)
    with pytest.raises(ValueError, match="Dtype of out must match that of input A"):
        sparse_matmul_to_dense(A, B, out=out)