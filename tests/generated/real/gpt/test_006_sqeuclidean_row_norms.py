import pytest
import numpy as np
from sklearn.metrics._pairwise_distances_reduction._dispatcher import sqeuclidean_row_norms

def test_sqeuclidean_row_norms_float64():
    X = np.array([[1.0, 2.0], [3.0, 4.0]], dtype=np.float64)
    expected = np.array([5.0, 25.0], dtype=np.float64)
    result = sqeuclidean_row_norms(X, num_threads=1)
    np.testing.assert_array_almost_equal(result, expected)

def test_sqeuclidean_row_norms_float32():
    X = np.array([[1.0, 2.0], [3.0, 4.0]], dtype=np.float32)
    expected = np.array([5.0, 25.0], dtype=np.float32)
    result = sqeuclidean_row_norms(X, num_threads=1)
    np.testing.assert_array_almost_equal(result, expected)

def test_sqeuclidean_row_norms_empty():
    X = np.array([[]], dtype=np.float64)
    expected = np.array([0.0], dtype=np.float64)
    result = sqeuclidean_row_norms(X, num_threads=1)
    np.testing.assert_array_almost_equal(result, expected)

def test_sqeuclidean_row_norms_single_row():
    X = np.array([[3.0, 4.0]], dtype=np.float64)
    expected = np.array([25.0], dtype=np.float64)
    result = sqeuclidean_row_norms(X, num_threads=1)
    np.testing.assert_array_almost_equal(result, expected)

def test_sqeuclidean_row_norms_invalid_dtype():
    X = np.array([[1, 2], [3, 4]], dtype=np.int32)
    with pytest.raises(ValueError, match="Only float64 or float32 datasets are supported at this time"):
        sqeuclidean_row_norms(X, num_threads=1)

def test_sqeuclidean_row_norms_multiple_threads():
    X = np.array([[1.0, 2.0], [3.0, 4.0]], dtype=np.float64)
    expected = np.array([5.0, 25.0], dtype=np.float64)
    result = sqeuclidean_row_norms(X, num_threads=2)
    np.testing.assert_array_almost_equal(result, expected)