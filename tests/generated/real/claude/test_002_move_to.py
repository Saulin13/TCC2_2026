import pytest
import numpy as np
from sklearn.utils._array_api import move_to
from sklearn.utils._array_api import get_namespace, get_namespace_and_device
import scipy.sparse as sp


def test_move_to_single_numpy_array():
    arr = np.array([1, 2, 3])
    result = move_to(arr, xp=np, device="cpu")
    assert isinstance(result, np.ndarray)
    np.testing.assert_array_equal(result, arr)


def test_move_to_multiple_numpy_arrays():
    arr1 = np.array([1, 2, 3])
    arr2 = np.array([4, 5, 6])
    result = move_to(arr1, arr2, xp=np, device="cpu")
    assert isinstance(result, tuple)
    assert len(result) == 2
    np.testing.assert_array_equal(result[0], arr1)
    np.testing.assert_array_equal(result[1], arr2)


def test_move_to_with_none():
    arr = np.array([1, 2, 3])
    result = move_to(arr, None, xp=np, device="cpu")
    assert isinstance(result, tuple)
    assert len(result) == 2
    np.testing.assert_array_equal(result[0], arr)
    assert result[1] is None


def test_move_to_only_none():
    result = move_to(None, xp=np, device="cpu")
    assert result is None


def test_move_to_sparse_array_with_numpy():
    sparse_arr = sp.csr_matrix([[1, 0, 2], [0, 3, 0]])
    result = move_to(sparse_arr, xp=np, device="cpu")
    assert sp.issparse(result)
    assert result is sparse_arr


def test_move_to_sparse_array_with_non_numpy_raises():
    sparse_arr = sp.csr_matrix([[1, 0, 2], [0, 3, 0]])
    try:
        import array_api_strict as xp_strict
        with pytest.raises(TypeError, match="Sparse arrays are only accepted"):
            move_to(sparse_arr, xp=xp_strict, device="cpu")
    except ImportError:
        pytest.skip("array_api_strict not available")


def test_move_to_mixed_sparse_and_dense():
    arr = np.array([1, 2, 3])
    sparse_arr = sp.csr_matrix([[1, 0, 2]])
    result = move_to(arr, sparse_arr, xp=np, device="cpu")
    assert isinstance(result, tuple)
    assert len(result) == 2
    np.testing.assert_array_equal(result[0], arr)
    assert sp.issparse(result[1])


def test_move_to_float64_to_float32_downcast():
    arr = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    result = move_to(arr, xp=np, device="cpu")
    # Behavior depends on device precision, but should not raise
    assert isinstance(result, np.ndarray)


def test_move_to_preserves_dtype_when_not_float64():
    arr = np.array([1, 2, 3], dtype=np.int32)
    result = move_to(arr, xp=np, device="cpu")
    assert result.dtype == np.int32


def test_move_to_empty_array():
    arr = np.array([])
    result = move_to(arr, xp=np, device="cpu")
    assert isinstance(result, np.ndarray)
    assert len(result) == 0


def test_move_to_multidimensional_array():
    arr = np.array([[1, 2], [3, 4], [5, 6]])
    result = move_to(arr, xp=np, device="cpu")
    assert isinstance(result, np.ndarray)
    np.testing.assert_array_equal(result, arr)
    assert result.shape == (3, 2)


def test_move_to_already_correct_namespace_and_device():
    arr = np.array([1, 2, 3])
    xp_arr, _, device_arr = get_namespace_and_device(arr)
    result = move_to(arr, xp=xp_arr, device=device_arr)
    # Should return the same array without conversion
    assert isinstance(result, np.ndarray)
    np.testing.assert_array_equal(result, arr)


def test_move_to_multiple_none_values():
    result = move_to(None, None, None, xp=np, device="cpu")
    assert isinstance(result, tuple)
    assert len(result) == 3
    assert all(x is None for x in result)


def test_move_to_mixed_none_and_arrays():
    arr1 = np.array([1, 2])
    arr2 = np.array([3, 4])
    result = move_to(arr1, None, arr2, None, xp=np, device="cpu")
    assert isinstance(result, tuple)
    assert len(result) == 4
    np.testing.assert_array_equal(result[0], arr1)
    assert result[1] is None
    np.testing.assert_array_equal(result[2], arr2)
    assert result[3] is None