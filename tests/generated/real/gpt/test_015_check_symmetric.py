import pytest
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.utils.validation import check_symmetric

def test_check_symmetric_normal_case():
    symmetric_array = np.array([[1, 2, 3], [2, 4, 5], [3, 5, 6]])
    result = check_symmetric(symmetric_array)
    expected = symmetric_array
    assert np.array_equal(result, expected)

def test_check_symmetric_non_symmetric_warning():
    non_symmetric_array = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    with pytest.warns(UserWarning, match="Array is not symmetric"):
        result = check_symmetric(non_symmetric_array)
    expected = np.array([[1, 3, 5], [3, 5, 7], [5, 7, 9]])
    assert np.array_equal(result, expected)

def test_check_symmetric_non_symmetric_exception():
    non_symmetric_array = np.array([[1, 2], [3, 4]])
    with pytest.raises(ValueError, match="Array must be symmetric"):
        check_symmetric(non_symmetric_array, raise_exception=True)

def test_check_symmetric_sparse_matrix():
    symmetric_sparse_array = csr_matrix([[1, 2, 3], [2, 4, 5], [3, 5, 6]])
    result = check_symmetric(symmetric_sparse_array)
    expected = symmetric_sparse_array
    assert (result != expected).nnz == 0

def test_check_symmetric_sparse_non_symmetric_warning():
    non_symmetric_sparse_array = csr_matrix([[1, 0, 0], [0, 1, 1], [0, 0, 1]])
    with pytest.warns(UserWarning, match="Array is not symmetric"):
        result = check_symmetric(non_symmetric_sparse_array)
    expected = csr_matrix([[1, 0, 0], [0, 1, 0.5], [0, 0.5, 1]])
    assert (result != expected).nnz == 0

def test_check_symmetric_edge_case_empty():
    empty_array = np.array([[]])
    with pytest.raises(ValueError, match="array must be 2-dimensional and square"):
        check_symmetric(empty_array)

def test_check_symmetric_edge_case_single_element():
    single_element_array = np.array([[42]])
    result = check_symmetric(single_element_array)
    expected = single_element_array
    assert np.array_equal(result, expected)