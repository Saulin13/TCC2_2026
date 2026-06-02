import pytest
import numpy as np
from scipy import sparse
from sklearn.utils.sparsefuncs import inplace_swap_column


def test_inplace_swap_column_csr_basic():
    indptr = np.array([0, 2, 3, 3, 3])
    indices = np.array([0, 2, 2])
    data = np.array([8, 2, 5])
    csr = sparse.csr_array((data, indices, indptr))
    
    inplace_swap_column(csr, 0, 1)
    
    expected = np.array([[0, 8, 2],
                        [0, 0, 5],
                        [0, 0, 0],
                        [0, 0, 0]])
    np.testing.assert_array_equal(csr.toarray(), expected)


def test_inplace_swap_column_csr_swap_same_column():
    indptr = np.array([0, 2, 3])
    indices = np.array([0, 2, 1])
    data = np.array([1, 2, 3])
    csr = sparse.csr_array((data, indices, indptr))
    original = csr.toarray().copy()
    
    inplace_swap_column(csr, 1, 1)
    
    np.testing.assert_array_equal(csr.toarray(), original)


def test_inplace_swap_column_csr_negative_indices():
    indptr = np.array([0, 2, 3, 3])
    indices = np.array([0, 2, 1])
    data = np.array([5, 7, 9])
    csr = sparse.csr_array((data, indices, indptr))
    
    inplace_swap_column(csr, -3, -1)
    
    expected = np.array([[7, 0, 5],
                        [0, 9, 0],
                        [0, 0, 0]])
    np.testing.assert_array_equal(csr.toarray(), expected)


def test_inplace_swap_column_csc_basic():
    indptr = np.array([0, 2, 2, 4])
    indices = np.array([0, 1, 0, 1])
    data = np.array([3, 4, 5, 6])
    csc = sparse.csc_array((data, indices, indptr))
    
    inplace_swap_column(csc, 0, 2)
    
    expected = np.array([[5, 0, 3],
                        [6, 0, 4]])
    np.testing.assert_array_equal(csc.toarray(), expected)


def test_inplace_swap_column_csc_middle_columns():
    indptr = np.array([0, 1, 2, 3, 4])
    indices = np.array([0, 1, 2, 0])
    data = np.array([1, 2, 3, 4])
    csc = sparse.csc_array((data, indices, indptr))
    
    inplace_swap_column(csc, 1, 2)
    
    expected = np.array([[1, 0, 0, 4],
                        [0, 0, 2, 0],
                        [0, 3, 0, 0]])
    np.testing.assert_array_equal(csc.toarray(), expected)


def test_inplace_swap_column_csc_negative_indices():
    indptr = np.array([0, 1, 2, 3])
    indices = np.array([0, 0, 1])
    data = np.array([10, 20, 30])
    csc = sparse.csc_array((data, indices, indptr))
    
    inplace_swap_column(csc, -2, -1)
    
    expected = np.array([[10, 0, 20],
                        [0, 30, 0]])
    np.testing.assert_array_equal(csc.toarray(), expected)


def test_inplace_swap_column_csr_empty_columns():
    indptr = np.array([0, 1, 1, 1])
    indices = np.array([1])
    data = np.array([5])
    csr = sparse.csr_array((data, indices, indptr))
    
    inplace_swap_column(csr, 0, 2)
    
    expected = np.array([[0, 5, 0],
                        [0, 0, 0],
                        [0, 0, 0]])
    np.testing.assert_array_equal(csr.toarray(), expected)


def test_inplace_swap_column_csc_empty_columns():
    indptr = np.array([0, 0, 1, 1])
    indices = np.array([0])
    data = np.array([7])
    csc = sparse.csc_array((data, indices, indptr))
    
    inplace_swap_column(csc, 0, 1)
    
    expected = np.array([[0, 7, 0]])
    np.testing.assert_array_equal(csc.toarray(), expected)


def test_inplace_swap_column_invalid_format():
    dense_array = np.array([[1, 2, 3], [4, 5, 6]])
    
    with pytest.raises(TypeError):
        inplace_swap_column(dense_array, 0, 1)


def test_inplace_swap_column_coo_format():
    row = np.array([0, 1, 2])
    col = np.array([0, 1, 2])
    data = np.array([1, 2, 3])
    coo = sparse.coo_array((data, (row, col)), shape=(3, 3))
    
    with pytest.raises(TypeError):
        inplace_swap_column(coo, 0, 1)


def test_inplace_swap_column_large_matrix():
    np.random.seed(42)
    dense = np.random.rand(100, 50)
    dense[dense < 0.9] = 0
    csr = sparse.csr_array(dense)
    
    inplace_swap_column(csr, 5, 25)
    
    expected = dense.copy()
    expected[:, [5, 25]] = expected[:, [25, 5]]
    np.testing.assert_array_almost_equal(csr.toarray(), expected)