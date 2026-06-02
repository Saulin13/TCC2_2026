import pytest
import numpy as np
import warnings
from scipy import sparse
from sklearn.utils.validation import check_symmetric


def test_check_symmetric_with_symmetric_array():
    symmetric_array = np.array([[0, 1, 2], [1, 0, 1], [2, 1, 0]])
    result = check_symmetric(symmetric_array)
    np.testing.assert_array_equal(result, symmetric_array)


def test_check_symmetric_with_asymmetric_array_default_warning():
    asymmetric_array = np.array([[0, 1, 2], [3, 0, 1], [4, 5, 0]])
    expected = 0.5 * (asymmetric_array + asymmetric_array.T)
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = check_symmetric(asymmetric_array)
        assert len(w) == 1
        assert "Array is not symmetric" in str(w[0].message)
    
    np.testing.assert_array_equal(result, expected)


def test_check_symmetric_with_asymmetric_array_no_warning():
    asymmetric_array = np.array([[0, 1, 2], [3, 0, 1], [4, 5, 0]])
    expected = 0.5 * (asymmetric_array + asymmetric_array.T)
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = check_symmetric(asymmetric_array, raise_warning=False)
        assert len(w) == 0
    
    np.testing.assert_array_equal(result, expected)


def test_check_symmetric_with_asymmetric_array_raise_exception():
    asymmetric_array = np.array([[0, 1, 2], [3, 0, 1], [4, 5, 0]])
    
    with pytest.raises(ValueError, match="Array must be symmetric"):
        check_symmetric(asymmetric_array, raise_exception=True)


def test_check_symmetric_with_custom_tolerance():
    almost_symmetric = np.array([[0, 1.0, 2.0], [1.0 + 1e-11, 0, 1.0], [2.0, 1.0, 0]])
    result = check_symmetric(almost_symmetric, tol=1e-10)
    np.testing.assert_array_equal(result, almost_symmetric)


def test_check_symmetric_with_custom_tolerance_fails():
    almost_symmetric = np.array([[0, 1.0, 2.0], [1.0 + 1e-8, 0, 1.0], [2.0, 1.0, 0]])
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = check_symmetric(almost_symmetric, tol=1e-10)
        assert len(w) == 1


def test_check_symmetric_with_non_square_array():
    non_square_array = np.array([[1, 2, 3], [4, 5, 6]])
    
    with pytest.raises(ValueError, match="array must be 2-dimensional and square"):
        check_symmetric(non_square_array)


def test_check_symmetric_with_1d_array():
    one_d_array = np.array([1, 2, 3])
    
    with pytest.raises(ValueError, match="array must be 2-dimensional and square"):
        check_symmetric(one_d_array)


def test_check_symmetric_with_3d_array():
    three_d_array = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
    
    with pytest.raises(ValueError, match="array must be 2-dimensional and square"):
        check_symmetric(three_d_array)


def test_check_symmetric_with_sparse_csr_symmetric():
    symmetric_array = np.array([[0, 1, 2], [1, 0, 1], [2, 1, 0]])
    sparse_symmetric = sparse.csr_matrix(symmetric_array)
    result = check_symmetric(sparse_symmetric)
    
    assert sparse.issparse(result)
    np.testing.assert_array_equal(result.toarray(), symmetric_array)


def test_check_symmetric_with_sparse_csr_asymmetric():
    asymmetric_array = np.array([[0, 1, 2], [3, 0, 1], [4, 5, 0]])
    sparse_asymmetric = sparse.csr_matrix(asymmetric_array)
    expected = 0.5 * (asymmetric_array + asymmetric_array.T)
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = check_symmetric(sparse_asymmetric)
        assert len(w) == 1
    
    assert sparse.issparse(result)
    np.testing.assert_array_almost_equal(result.toarray(), expected)


def test_check_symmetric_with_sparse_coo():
    symmetric_array = np.array([[0, 1, 2], [1, 0, 1], [2, 1, 0]])
    sparse_symmetric = sparse.coo_matrix(symmetric_array)
    result = check_symmetric(sparse_symmetric)
    
    assert sparse.issparse(result)
    np.testing.assert_array_equal(result.toarray(), symmetric_array)


def test_check_symmetric_with_sparse_lil_asymmetric():
    asymmetric_array = np.array([[0, 1, 2], [3, 0, 1], [4, 5, 0]])
    sparse_asymmetric = sparse.lil_matrix(asymmetric_array)
    expected = 0.5 * (asymmetric_array + asymmetric_array.T)
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        result = check_symmetric(sparse_asymmetric)
        assert len(w) == 1
    
    assert sparse.issparse(result)
    np.testing.assert_array_almost_equal(result.toarray(), expected)


def test_check_symmetric_with_float_array():
    symmetric_float = np.array([[1.5, 2.3, 3.7], [2.3, 4.2, 5.1], [3.7, 5.1, 6.8]])
    result = check_symmetric(symmetric_float)
    np.testing.assert_array_equal(result, symmetric_float)


def test_check_symmetric_single_element():
    single_element = np.array([[5]])
    result = check_symmetric(single_element)
    np.testing.assert_array_equal(result, single_element)