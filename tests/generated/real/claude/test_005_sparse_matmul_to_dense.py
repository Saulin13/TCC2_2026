import pytest
import numpy as np
from scipy import sparse as sp
from sklearn.utils.sparsefuncs import sparse_matmul_to_dense


def test_sparse_matmul_to_dense_csr_csr_basic():
    A = sp.csr_matrix([[1.0, 2.0], [3.0, 4.0]])
    B = sp.csr_matrix([[5.0, 6.0], [7.0, 8.0]])
    result = sparse_matmul_to_dense(A, B)
    expected = np.array([[19.0, 22.0], [43.0, 50.0]])
    np.testing.assert_array_almost_equal(result, expected)


def test_sparse_matmul_to_dense_csc_csc_basic():
    A = sp.csc_matrix([[1.0, 2.0], [3.0, 4.0]])
    B = sp.csc_matrix([[5.0, 6.0], [7.0, 8.0]])
    result = sparse_matmul_to_dense(A, B)
    expected = np.array([[19.0, 22.0], [43.0, 50.0]])
    np.testing.assert_array_almost_equal(result, expected)


def test_sparse_matmul_to_dense_csr_csc_mixed():
    A = sp.csr_matrix([[1.0, 2.0], [3.0, 4.0]])
    B = sp.csc_matrix([[5.0, 6.0], [7.0, 8.0]])
    result = sparse_matmul_to_dense(A, B)
    expected = np.array([[19.0, 22.0], [43.0, 50.0]])
    np.testing.assert_array_almost_equal(result, expected)


def test_sparse_matmul_to_dense_csc_csr_mixed():
    A = sp.csc_matrix([[1.0, 2.0], [3.0, 4.0]])
    B = sp.csr_matrix([[5.0, 6.0], [7.0, 8.0]])
    result = sparse_matmul_to_dense(A, B)
    expected = np.array([[19.0, 22.0], [43.0, 50.0]])
    np.testing.assert_array_almost_equal(result, expected)


def test_sparse_matmul_to_dense_with_zeros():
    A = sp.csr_matrix([[1.0, 0.0], [0.0, 2.0]])
    B = sp.csr_matrix([[3.0, 0.0], [0.0, 4.0]])
    result = sparse_matmul_to_dense(A, B)
    expected = np.array([[3.0, 0.0], [0.0, 8.0]])
    np.testing.assert_array_almost_equal(result, expected)


def test_sparse_matmul_to_dense_float32():
    A = sp.csr_matrix([[1.0, 2.0], [3.0, 4.0]], dtype=np.float32)
    B = sp.csr_matrix([[5.0, 6.0], [7.0, 8.0]], dtype=np.float32)
    result = sparse_matmul_to_dense(A, B)
    expected = np.array([[19.0, 22.0], [43.0, 50.0]], dtype=np.float32)
    np.testing.assert_array_almost_equal(result, expected)
    assert result.dtype == np.float32


def test_sparse_matmul_to_dense_with_out_parameter():
    A = sp.csr_matrix([[1.0, 2.0], [3.0, 4.0]])
    B = sp.csr_matrix([[5.0, 6.0], [7.0, 8.0]])
    out = np.zeros((2, 2), dtype=np.float64)
    result = sparse_matmul_to_dense(A, B, out=out)
    expected = np.array([[19.0, 22.0], [43.0, 50.0]])
    np.testing.assert_array_almost_equal(result, expected)
    assert result is out


def test_sparse_matmul_to_dense_rectangular_matrices():
    A = sp.csr_matrix([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    B = sp.csr_matrix([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    result = sparse_matmul_to_dense(A, B)
    expected = np.array([[22.0, 28.0], [49.0, 64.0]])
    np.testing.assert_array_almost_equal(result, expected)


def test_sparse_matmul_to_dense_single_element():
    A = sp.csr_matrix([[2.0]])
    B = sp.csr_matrix([[3.0]])
    result = sparse_matmul_to_dense(A, B)
    expected = np.array([[6.0]])
    np.testing.assert_array_almost_equal(result, expected)


def test_sparse_matmul_to_dense_invalid_A_not_sparse():
    A = np.array([[1.0, 2.0], [3.0, 4.0]])
    B = sp.csr_matrix([[5.0, 6.0], [7.0, 8.0]])
    with pytest.raises(ValueError, match="Input 'A' must be a sparse 2-dim CSC or CSR array"):
        sparse_matmul_to_dense(A, B)


def test_sparse_matmul_to_dense_invalid_B_not_sparse():
    A = sp.csr_matrix([[1.0, 2.0], [3.0, 4.0]])
    B = np.array([[5.0, 6.0], [7.0, 8.0]])
    with pytest.raises(ValueError, match="Input 'B' must be a sparse 2-dim CSC or CSR array"):
        sparse_matmul_to_dense(A, B)


def test_sparse_matmul_to_dense_invalid_format():
    A = sp.coo_matrix([[1.0, 2.0], [3.0, 4.0]])
    B = sp.csr_matrix([[5.0, 6.0], [7.0, 8.0]])
    with pytest.raises(ValueError, match="Input 'A' must be a sparse 2-dim CSC or CSR array"):
        sparse_matmul_to_dense(A, B)


def test_sparse_matmul_to_dense_shape_mismatch():
    A = sp.csr_matrix([[1.0, 2.0], [3.0, 4.0]])
    B = sp.csr_matrix([[5.0, 6.0], [7.0, 8.0], [9.0, 10.0]])
    with pytest.raises(ValueError, match="Shapes must fulfil A.shape\\[1\\] == B.shape\\[0\\]"):
        sparse_matmul_to_dense(A, B)


def test_sparse_matmul_to_dense_dtype_mismatch():
    A = sp.csr_matrix([[1.0, 2.0], [3.0, 4.0]], dtype=np.float32)
    B = sp.csr_matrix([[5.0, 6.0], [7.0, 8.0]], dtype=np.float64)
    with pytest.raises(ValueError, match="Dtype of A and B must be the same"):
        sparse_matmul_to_dense(A, B)


def test_sparse_matmul_to_dense_invalid_dtype():
    A = sp.csr_matrix([[1, 2], [3, 4]], dtype=np.int32)
    B = sp.csr_matrix([[5, 6], [7, 8]], dtype=np.int32)
    with pytest.raises(ValueError, match="Dtype of A and B must be the same"):
        sparse_matmul_to_dense(A, B)


def test_sparse_matmul_to_dense_out_wrong_shape():
    A = sp.csr_matrix([[1.0, 2.0], [3.0, 4.0]])
    B = sp.csr_matrix([[5.0, 6.0], [7.0, 8.0]])
    out = np.zeros((3, 3), dtype=np.float64)
    with pytest.raises(ValueError, match="Shape of out must be"):
        sparse_matmul_to_dense(A, B, out=out)


def test_sparse_matmul_to_dense_out_wrong_dtype():
    A = sp.csr_matrix([[1.0, 2.0], [3.0, 4.0]], dtype=np.float64)
    B = sp.csr_matrix([[5.0, 6.0], [7.0, 8.0]], dtype=np.float64)
    out = np.zeros((2, 2), dtype=np.float32)
    with pytest.raises(ValueError, match="Dtype of out must match that of input A"):
        sparse_matmul_to_dense(A, B, out=out)