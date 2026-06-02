import pytest
import numpy as np
from scipy import sparse
from sklearn.utils.sparsefuncs import inplace_swap_column

def test_inplace_swap_column_normal_case():
    indptr = np.array([0, 2, 3, 3, 3])
    indices = np.array([0, 2, 2])
    data = np.array([8, 2, 5])
    csr = sparse.csr_matrix((data, indices, indptr))
    inplace_swap_column(csr, 0, 1)
    expected = np.array([[0, 8, 2],
                         [0, 0, 5],
                         [0, 0, 0],
                         [0, 0, 0]])
    assert np.array_equal(csr.todense(), expected)

def test_inplace_swap_column_edge_case_same_column():
    indptr = np.array([0, 2, 3, 3, 3])
    indices = np.array([0, 2, 2])
    data = np.array([8, 2, 5])
    csr = sparse.csr_matrix((data, indices, indptr))
    inplace_swap_column(csr, 0, 0)
    expected = np.array([[8, 0, 2],
                         [0, 0, 5],
                         [0, 0, 0],
                         [0, 0, 0]])
    assert np.array_equal(csr.todense(), expected)

def test_inplace_swap_column_edge_case_negative_index():
    indptr = np.array([0, 2, 3, 3, 3])
    indices = np.array([0, 2, 2])
    data = np.array([8, 2, 5])
    csr = sparse.csr_matrix((data, indices, indptr))
    inplace_swap_column(csr, -3, -2)
    expected = np.array([[0, 8, 2],
                         [0, 0, 5],
                         [0, 0, 0],
                         [0, 0, 0]])
    assert np.array_equal(csr.todense(), expected)

def test_inplace_swap_column_failure_non_sparse_matrix():
    X = np.array([[1, 2], [3, 4]])
    with pytest.raises(TypeError):
        inplace_swap_column(X, 0, 1)

def test_inplace_swap_column_failure_out_of_bounds():
    indptr = np.array([0, 2, 3, 3, 3])
    indices = np.array([0, 2, 2])
    data = np.array([8, 2, 5])
    csr = sparse.csr_matrix((data, indices, indptr))
    with pytest.raises(IndexError):
        inplace_swap_column(csr, 0, 5)