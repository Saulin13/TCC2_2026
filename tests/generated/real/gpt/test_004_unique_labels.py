import pytest
import numpy as np
from sklearn.utils.multiclass import unique_labels

def test_unique_labels_single_list():
    result = unique_labels([3, 5, 5, 5, 7, 7])
    expected = np.array([3, 5, 7])
    assert np.array_equal(result, expected)

def test_unique_labels_multiple_lists():
    result = unique_labels([1, 2, 3, 4], [2, 2, 3, 4])
    expected = np.array([1, 2, 3, 4])
    assert np.array_equal(result, expected)

def test_unique_labels_disjoint_lists():
    result = unique_labels([1, 2, 10], [5, 11])
    expected = np.array([1, 2, 5, 10, 11])
    assert np.array_equal(result, expected)

def test_unique_labels_empty_input():
    with pytest.raises(ValueError, match="No argument has been passed."):
        unique_labels()

def test_unique_labels_mixed_types():
    with pytest.raises(ValueError, match="Mix of label input types"):
        unique_labels([1, 2, 3], ["a", "b", "c"])

def test_unique_labels_mixed_target_types():
    with pytest.raises(ValueError, match="Mix type of y not allowed"):
        unique_labels([1, 2, 3], [[0, 1], [1, 0]])

def test_unique_labels_multilabel_indicator_different_sizes():
    with pytest.raises(ValueError, match="Multi-label binary indicator input with different numbers of labels"):
        unique_labels([[0, 1], [1, 0]], [[1, 0, 0], [0, 1, 1]])

def test_unique_labels_single_element_lists():
    result = unique_labels([1], [2], [3])
    expected = np.array([1, 2, 3])
    assert np.array_equal(result, expected)

def test_unique_labels_with_duplicates():
    result = unique_labels([1, 1, 2, 2], [2, 3, 3, 4])
    expected = np.array([1, 2, 3, 4])
    assert np.array_equal(result, expected)