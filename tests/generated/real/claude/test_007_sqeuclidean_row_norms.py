import pytest
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.metrics._pairwise_distances_reduction._dispatcher import sqeuclidean_row_norms


def test_sqeuclidean_row_norms_float64_dense():
    X = np.array([[1.0, 2.0, 3.0],
                  [4.0, 5.0, 6.0],
                  [7.0, 8.0, 9.0]], dtype=np.float64, order='C')
    result = sqeuclidean_row_norms(X, num_threads=1)
    expected = np.array([14.0, 77.0, 194.0], dtype=np.float64)
    np.testing.assert_array_almost_equal(result, expected)


def test_sqeuclidean_row_norms_float32_dense():
    X = np.array([[1.0, 2.0, 3.0],
                  [4.0, 5.0, 6.0]], dtype=np.float32, order='C')
    result = sqeuclidean_row_norms(X, num_threads=1)
    expected = np.array([14.0, 77.0], dtype=np.float32)
    np.testing.assert_array_almost_equal(result, expected)


def test_sqeuclidean_row_norms_single_row():
    X = np.array([[3.0, 4.0]], dtype=np.float64, order='C')
    result = sqeuclidean_row_norms(X, num_threads=1)
    expected = np.array([25.0], dtype=np.float64)
    np.testing.assert_array_almost_equal(result, expected)


def test_sqeuclidean_row_norms_single_column():
    X = np.array([[3.0], [4.0], [5.0]], dtype=np.float64, order='C')
    result = sqeuclidean_row_norms(X, num_threads=1)
    expected = np.array([9.0, 16.0, 25.0], dtype=np.float64)
    np.testing.assert_array_almost_equal(result, expected)


def test_sqeuclidean_row_norms_zeros():
    X = np.zeros((3, 4), dtype=np.float64, order='C')
    result = sqeuclidean_row_norms(X, num_threads=1)
    expected = np.zeros(3, dtype=np.float64)
    np.testing.assert_array_almost_equal(result, expected)


def test_sqeuclidean_row_norms_negative_values():
    X = np.array([[-1.0, -2.0, -3.0],
                  [1.0, -2.0, 3.0]], dtype=np.float64, order='C')
    result = sqeuclidean_row_norms(X, num_threads=1)
    expected = np.array([14.0, 14.0], dtype=np.float64)
    np.testing.assert_array_almost_equal(result, expected)


def test_sqeuclidean_row_norms_multiple_threads():
    X = np.array([[1.0, 2.0, 3.0],
                  [4.0, 5.0, 6.0],
                  [7.0, 8.0, 9.0]], dtype=np.float64, order='C')
    result = sqeuclidean_row_norms(X, num_threads=2)
    expected = np.array([14.0, 77.0, 194.0], dtype=np.float64)
    np.testing.assert_array_almost_equal(result, expected)


def test_sqeuclidean_row_norms_csr_matrix_float64():
    X_dense = np.array([[1.0, 0.0, 3.0],
                        [0.0, 5.0, 0.0],
                        [7.0, 0.0, 9.0]], dtype=np.float64)
    X = csr_matrix(X_dense)
    result = sqeuclidean_row_norms(X, num_threads=1)
    expected = np.array([10.0, 25.0, 130.0], dtype=np.float64)
    np.testing.assert_array_almost_equal(result, expected)


def test_sqeuclidean_row_norms_csr_matrix_float32():
    X_dense = np.array([[1.0, 0.0, 3.0],
                        [0.0, 5.0, 0.0]], dtype=np.float32)
    X = csr_matrix(X_dense)
    result = sqeuclidean_row_norms(X, num_threads=1)
    expected = np.array([10.0, 25.0], dtype=np.float32)
    np.testing.assert_array_almost_equal(result, expected)


def test_sqeuclidean_row_norms_invalid_dtype():
    X = np.array([[1, 2, 3],
                  [4, 5, 6]], dtype=np.int32, order='C')
    with pytest.raises(ValueError, match="Only float64 or float32 datasets are supported"):
        sqeuclidean_row_norms(X, num_threads=1)


def test_sqeuclidean_row_norms_invalid_dtype_float16():
    X = np.array([[1.0, 2.0, 3.0],
                  [4.0, 5.0, 6.0]], dtype=np.float16, order='C')
    with pytest.raises(ValueError, match="Only float64 or float32 datasets are supported"):
        sqeuclidean_row_norms(X, num_threads=1)


def test_sqeuclidean_row_norms_large_values():
    X = np.array([[100.0, 200.0, 300.0],
                  [1000.0, 2000.0, 3000.0]], dtype=np.float64, order='C')
    result = sqeuclidean_row_norms(X, num_threads=1)
    expected = np.array([140000.0, 14000000.0], dtype=np.float64)
    np.testing.assert_array_almost_equal(result, expected)


def test_sqeuclidean_row_norms_fractional_values():
    X = np.array([[0.5, 0.5],
                  [0.1, 0.2]], dtype=np.float64, order='C')
    result = sqeuclidean_row_norms(X, num_threads=1)
    expected = np.array([0.5, 0.05], dtype=np.float64)
    np.testing.assert_array_almost_equal(result, expected)