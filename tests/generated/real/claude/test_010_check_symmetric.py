import pytest
import numpy as np
import warnings
from scipy import sparse
from sklearn.utils.validation import check_symmetric


def test_check_symmetric_with_symmetric_array():
    """Test with a symmetric numpy array."""
    symmetric_array = np.array([[0, 1, 2], [1, 0, 1], [2, 1, 0]])
    result = check_symmetric(symmetric_array)
    np.testing.assert_array_equal(result, symmetric_array)


def test_check_symmetric_with_asymmetric_array_default():
    """Test with an asymmetric array, should return symmetrized version with warning."""
    asymmetric_array = np.array([[0, 1, 2], [3, 0, 1], [4, 5, 0]])
    expected = np.array([[0, 2, 3], [2, 0, 3], [3, 3, 0]])
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = check_symmetric(asymmetric_array)
        assert len(w) == 1
        assert "Array is not symmetric" in str(w[0].message)
    
    np.testing.assert_array_equal(result, expected)


def test_check_symmetric_with_asymmetric_array_no_warning():
    """Test with an asymmetric array with raise_warning=False."""
    asymmetric_array = np.array([[0, 1, 2], [3, 0, 1], [4, 5, 0]])
    expected = np.array([[0, 2, 3], [2, 0, 3], [3, 3, 0]])
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = check_symmetric(asymmetric_array, raise_warning=False)
        assert len(w) == 0
    
    np.testing.assert_array_equal(result, expected)


def test_check_symmetric_with_asymmetric_array_raise_exception():
    """Test that exception is raised when raise_exception=True."""
    asymmetric_array = np.array([[0, 1, 2], [3, 0, 1], [4, 5, 0]])
    
    with pytest.raises(ValueError, match="Array must be symmetric"):
        check_symmetric(asymmetric_array, raise_exception=True)


def test_check_symmetric_with_custom_tolerance():
    """Test with custom tolerance."""
    almost_symmetric = np.array([[0, 1.0, 2.0], [1.0 + 1e-11, 0, 1.0], [2.0, 1.0, 0]])
    result = check_symmetric(almost_symmetric, tol=1e-10)
    np.testing.assert_array_equal(result, almost_symmetric)


def test_check_symmetric_with_tolerance_exceeded():
    """Test when difference exceeds tolerance."""
    almost_symmetric = np.array([[0, 1.0, 2.0], [1.0 + 1e-9, 0, 1.0], [2.0, 1.0, 0]])
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = check_symmetric(almost_symmetric, tol=1e-10)
        assert len(w) == 1


def test_check_symmetric_with_sparse_csr_symmetric():
    """Test with a symmetric sparse CSR matrix."""
    symmetric_array = np.array([[0, 1, 2], [1, 0, 1], [2, 1, 0]])
    sparse_symmetric = sparse.csr_matrix(symmetric_array)
    result = check_symmetric(sparse_symmetric)
    np.testing.assert_array_equal(result.toarray(), symmetric_array)


def test_check_symmetric_with_sparse_csr_asymmetric():
    """Test with an asymmetric sparse CSR matrix."""
    asymmetric_array = np.array([[0, 1, 2], [3, 0, 1], [4, 5, 0]])
    sparse_asymmetric = sparse.csr_matrix(asymmetric_array)
    expected = np.array([[0, 2, 3], [2, 0, 3], [3, 3, 0]])
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = check_symmetric(sparse_asymmetric)
        assert len(w) == 1
    
    np.testing.assert_array_equal(result.toarray(), expected)


def test_check_symmetric_with_sparse_coo():
    """Test with a sparse COO matrix."""
    symmetric_array = np.array([[0, 1, 2], [1, 0, 1], [2, 1, 0]])
    sparse_symmetric = sparse.coo_matrix(symmetric_array)
    result = check_symmetric(sparse_symmetric)
    np.testing.assert_array_equal(result.toarray(), symmetric_array)


def test_check_symmetric_with_non_square_array():
    """Test that ValueError is raised for non-square array."""
    non_square = np.array([[1, 2, 3], [4, 5, 6]])
    
    with pytest.raises(ValueError, match="array must be 2-dimensional and square"):
        check_symmetric(non_square)


def test_check_symmetric_with_1d_array():
    """Test that ValueError is raised for 1D array."""
    one_d_array = np.array([1, 2, 3])
    
    with pytest.raises(ValueError, match="array must be 2-dimensional and square"):
        check_symmetric(one_d_array)


def test_check_symmetric_with_3d_array():
    """Test that ValueError is raised for 3D array."""
    three_d_array = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
    
    with pytest.raises(ValueError, match="array must be 2-dimensional and square"):
        check_symmetric(three_d_array)


def test_check_symmetric_with_single_element():
    """Test with a 1x1 array."""
    single_element = np.array([[5]])
    result = check_symmetric(single_element)
    np.testing.assert_array_equal(result, single_element)


def test_check_symmetric_with_zeros():
    """Test with a zero matrix."""
    zero_matrix = np.zeros((3, 3))
    result = check_symmetric(zero_matrix)
    np.testing.assert_array_equal(result, zero_matrix)


def test_check_symmetric_with_identity():
    """Test with an identity matrix."""
    identity = np.eye(4)
    result = check_symmetric(identity)
    np.testing.assert_array_equal(result, identity)