import pytest
import numpy as np
from sklearn.utils._unique import cached_unique


def test_cached_unique_single_array():
    y = np.array([1, 2, 2, 3, 1, 4])
    result = cached_unique(y)
    expected = np.array([1, 2, 3, 4])
    np.testing.assert_array_equal(result, expected)


def test_cached_unique_multiple_arrays():
    y1 = np.array([1, 2, 2, 3, 1])
    y2 = np.array([5, 5, 6, 7])
    result = cached_unique(y1, y2)
    assert isinstance(result, tuple)
    assert len(result) == 2
    np.testing.assert_array_equal(result[0], np.array([1, 2, 3]))
    np.testing.assert_array_equal(result[1], np.array([5, 6, 7]))


def test_cached_unique_empty_array():
    y = np.array([])
    result = cached_unique(y)
    np.testing.assert_array_equal(result, np.array([]))


def test_cached_unique_single_element():
    y = np.array([5])
    result = cached_unique(y)
    np.testing.assert_array_equal(result, np.array([5]))


def test_cached_unique_all_same_values():
    y = np.array([7, 7, 7, 7])
    result = cached_unique(y)
    np.testing.assert_array_equal(result, np.array([7]))


def test_cached_unique_already_unique():
    y = np.array([1, 2, 3, 4, 5])
    result = cached_unique(y)
    np.testing.assert_array_equal(result, np.array([1, 2, 3, 4, 5]))


def test_cached_unique_string_array():
    y = np.array(['a', 'b', 'a', 'c', 'b'])
    result = cached_unique(y)
    np.testing.assert_array_equal(result, np.array(['a', 'b', 'c']))


def test_cached_unique_float_array():
    y = np.array([1.5, 2.3, 1.5, 3.7, 2.3])
    result = cached_unique(y)
    np.testing.assert_array_equal(result, np.array([1.5, 2.3, 3.7]))


def test_cached_unique_negative_numbers():
    y = np.array([-3, -1, -3, 0, 2, -1])
    result = cached_unique(y)
    np.testing.assert_array_equal(result, np.array([-3, -1, 0, 2]))


def test_cached_unique_three_arrays():
    y1 = np.array([1, 1, 2])
    y2 = np.array([3, 4, 3])
    y3 = np.array([5, 5, 5])
    result = cached_unique(y1, y2, y3)
    assert isinstance(result, tuple)
    assert len(result) == 3
    np.testing.assert_array_equal(result[0], np.array([1, 2]))
    np.testing.assert_array_equal(result[1], np.array([3, 4]))
    np.testing.assert_array_equal(result[2], np.array([5]))


def test_cached_unique_with_xp_parameter():
    y = np.array([1, 2, 2, 3, 1])
    result = cached_unique(y, xp=np)
    np.testing.assert_array_equal(result, np.array([1, 2, 3]))


def test_cached_unique_2d_array():
    y = np.array([[1, 2], [1, 2], [3, 4]])
    result = cached_unique(y)
    expected = np.array([[1, 2], [3, 4]])
    np.testing.assert_array_equal(result, expected)


def test_cached_unique_boolean_array():
    y = np.array([True, False, True, False, True])
    result = cached_unique(y)
    np.testing.assert_array_equal(result, np.array([False, True]))


def test_cached_unique_with_nan():
    y = np.array([1.0, np.nan, 2.0, np.nan, 3.0])
    result = cached_unique(y)
    assert len(result) == 4
    assert np.isnan(result[-1])
    np.testing.assert_array_equal(result[:-1], np.array([1.0, 2.0, 3.0]))