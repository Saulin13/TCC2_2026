import pytest
import numpy as np
from scipy.sparse import csr_matrix, csc_matrix, coo_matrix
from sklearn.utils.multiclass import unique_labels


def test_unique_labels_single_array():
    result = unique_labels([3, 5, 5, 5, 7, 7])
    expected = np.array([3, 5, 7])
    np.testing.assert_array_equal(result, expected)


def test_unique_labels_multiple_arrays():
    result = unique_labels([1, 2, 3, 4], [2, 2, 3, 4])
    expected = np.array([1, 2, 3, 4])
    np.testing.assert_array_equal(result, expected)


def test_unique_labels_disjoint_arrays():
    result = unique_labels([1, 2, 10], [5, 11])
    expected = np.array([1, 2, 5, 10, 11])
    np.testing.assert_array_equal(result, expected)


def test_unique_labels_numpy_arrays():
    result = unique_labels(np.array([1, 2, 3]), np.array([3, 4, 5]))
    expected = np.array([1, 2, 3, 4, 5])
    np.testing.assert_array_equal(result, expected)


def test_unique_labels_binary():
    result = unique_labels([0, 1, 1, 0])
    expected = np.array([0, 1])
    np.testing.assert_array_equal(result, expected)


def test_unique_labels_string_labels():
    result = unique_labels(['cat', 'dog', 'cat', 'bird'])
    expected = np.array(['bird', 'cat', 'dog'])
    np.testing.assert_array_equal(result, expected)


def test_unique_labels_string_multiple_arrays():
    result = unique_labels(['a', 'b'], ['c', 'd'])
    expected = np.array(['a', 'b', 'c', 'd'])
    np.testing.assert_array_equal(result, expected)


def test_unique_labels_single_value():
    result = unique_labels([5, 5, 5])
    expected = np.array([5])
    np.testing.assert_array_equal(result, expected)


def test_unique_labels_multilabel_indicator():
    y1 = np.array([[1, 0, 1], [0, 1, 0]])
    y2 = np.array([[1, 1, 0], [0, 0, 1]])
    result = unique_labels(y1, y2)
    expected = np.array([0, 1])
    np.testing.assert_array_equal(result, expected)


def test_unique_labels_sparse_multilabel():
    y1 = csr_matrix([[1, 0, 1], [0, 1, 0]])
    y2 = csr_matrix([[1, 1, 0], [0, 0, 1]])
    result = unique_labels(y1, y2)
    expected = np.array([0, 1])
    np.testing.assert_array_equal(result, expected)


def test_unique_labels_sparse_csc():
    y1 = csc_matrix([[1, 0, 1], [0, 1, 0]])
    y2 = csc_matrix([[1, 1, 0], [0, 0, 1]])
    result = unique_labels(y1, y2)
    expected = np.array([0, 1])
    np.testing.assert_array_equal(result, expected)


def test_unique_labels_sparse_coo():
    y1 = coo_matrix([[1, 0, 1], [0, 1, 0]])
    y2 = coo_matrix([[1, 1, 0], [0, 0, 1]])
    result = unique_labels(y1, y2)
    expected = np.array([0, 1])
    np.testing.assert_array_equal(result, expected)


def test_unique_labels_no_arguments():
    with pytest.raises(ValueError, match="No argument has been passed"):
        unique_labels()


def test_unique_labels_mixed_types():
    with pytest.raises(ValueError, match="Mix type of y not allowed"):
        unique_labels([1, 2, 3], [[1, 0], [0, 1]])


def test_unique_labels_mixed_string_and_number():
    with pytest.raises(ValueError, match="Mix of label input types"):
        unique_labels([1, 2, 3], ['a', 'b', 'c'])


def test_unique_labels_multilabel_different_sizes():
    y1 = np.array([[1, 0, 1], [0, 1, 0]])
    y2 = np.array([[1, 0], [0, 1]])
    with pytest.raises(ValueError, match="different numbers of labels"):
        unique_labels(y1, y2)


def test_unique_labels_negative_values():
    result = unique_labels([-1, 0, 1, 2])
    expected = np.array([-1, 0, 1, 2])
    np.testing.assert_array_equal(result, expected)


def test_unique_labels_float_values():
    result = unique_labels([1.0, 2.0, 3.0, 2.0])
    expected = np.array([1.0, 2.0, 3.0])
    np.testing.assert_array_equal(result, expected)


def test_unique_labels_empty_array_content():
    result = unique_labels([0], [1])
    expected = np.array([0, 1])
    np.testing.assert_array_equal(result, expected)