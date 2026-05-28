import pytest
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.utils.validation import check_symmetric

def test_check_symmetric_normal_case():
    symmetric_array = np.array([[0, 1, 2], [1, 0, 1], [2, 1, 0]])
    result = check_symmetric(symmetric_array)
    expected = np.array([[0, 1, 2], [1, 0, 1], [2, 1, 0]])
    assert np.array_equal(result, expected)

def test_check_symmetric_sparse_case():
    symmetric_array = np.array([[0, 1, 2], [1, 0, 1], [2, 1, 0]])
    sparse_symmetric_array = csr_matrix(symmetric_array)
    result = check_symmetric(sparse_symmetric_array)
    assert (result != sparse_symmetric_array).nnz == 0

def test_check_symmetric_non_symmetric_warning():
    non_symmetric_array = np.array([[0, 2, 2], [1, 0, 1], [2, 1, 0]])
    with pytest.warns(UserWarning, match="Array is not symmetric"):
        result = check_symmetric(non_symmetric_array)
    expected = np.array([[0, 1.5, 2], [1.5, 0, 1], [2, 1, 0]])
    assert np.allclose(result, expected)

def test_check_symmetric_non_symmetric_exception():
    non_symmetric_array = np.array([[0, 2, 2], [1, 0, 1], [2, 1, 0]])
    with pytest.raises(ValueError, match="Array must be symmetric"):
        check_symmetric(non_symmetric_array, raise_exception=True)

def test_check_symmetric_edge_case_single_element():
    single_element_array = np.array([[1]])
    result = check_symmetric(single_element_array)
    expected = np.array([[1]])
    assert np.array_equal(result, expected)

def test_check_symmetric_edge_case_empty_array():
    empty_array = np.array([[]])
    with pytest.raises(ValueError, match="array must be 2-dimensional and square"):
        check_symmetric(empty_array)

def test_check_symmetric_edge_case_non_square():
    non_square_array = np.array([[1, 2, 3], [4, 5, 6]])
    with pytest.raises(ValueError, match="array must be 2-dimensional and square"):
        check_symmetric(non_square_array)