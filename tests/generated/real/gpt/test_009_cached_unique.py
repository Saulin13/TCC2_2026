import pytest
import numpy as np
from sklearn.utils._unique import cached_unique

def test_cached_unique_single_array():
    # Normal case: single array with duplicates
    input_array = np.array([1, 2, 2, 3, 4, 4, 5])
    expected_output = np.array([1, 2, 3, 4, 5])
    result = cached_unique(input_array)
    assert np.array_equal(result, expected_output)

def test_cached_unique_multiple_arrays():
    # Normal case: multiple arrays with duplicates
    input_array1 = np.array([1, 2, 2, 3])
    input_array2 = np.array([4, 4, 5, 6])
    expected_output1 = np.array([1, 2, 3])
    expected_output2 = np.array([4, 5, 6])
    result = cached_unique(input_array1, input_array2)
    assert len(result) == 2
    assert np.array_equal(result[0], expected_output1)
    assert np.array_equal(result[1], expected_output2)

def test_cached_unique_empty_array():
    # Edge case: empty array
    input_array = np.array([])
    expected_output = np.array([])
    result = cached_unique(input_array)
    assert np.array_equal(result, expected_output)

def test_cached_unique_single_element_array():
    # Edge case: single element array
    input_array = np.array([42])
    expected_output = np.array([42])
    result = cached_unique(input_array)
    assert np.array_equal(result, expected_output)

def test_cached_unique_no_duplicates():
    # Normal case: array with no duplicates
    input_array = np.array([1, 2, 3, 4, 5])
    expected_output = np.array([1, 2, 3, 4, 5])
    result = cached_unique(input_array)
    assert np.array_equal(result, expected_output)

def test_cached_unique_non_array_input():
    # Failure case: non-array input
    with pytest.raises(TypeError):
        cached_unique("not an array")