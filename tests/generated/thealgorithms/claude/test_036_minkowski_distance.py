import pytest
from maths.minkowski_distance import minkowski_distance


def test_minkowski_distance_manhattan():
    assert minkowski_distance([1.0, 1.0], [2.0, 2.0], 1) == 2.0


def test_minkowski_distance_euclidean():
    assert minkowski_distance([1.0, 2.0, 3.0, 4.0], [5.0, 6.0, 7.0, 8.0], 2) == 8.0


def test_minkowski_distance_order_3():
    result = minkowski_distance([5.0], [0.0], 3)
    assert abs(result - 5.0) < 1e-9


def test_minkowski_distance_same_points():
    assert minkowski_distance([1.0, 2.0, 3.0], [1.0, 2.0, 3.0], 2) == 0.0


def test_minkowski_distance_negative_coordinates():
    assert minkowski_distance([-1.0, -2.0], [1.0, 2.0], 1) == 6.0


def test_minkowski_distance_mixed_coordinates():
    result = minkowski_distance([-3.0, 4.0], [3.0, -2.0], 2)
    expected = (36.0 + 36.0) ** 0.5
    assert abs(result - expected) < 1e-9


def test_minkowski_distance_high_order():
    result = minkowski_distance([0.0, 0.0], [1.0, 1.0], 10)
    expected = (1.0 + 1.0) ** 0.1
    assert abs(result - expected) < 1e-9


def test_minkowski_distance_single_dimension():
    assert minkowski_distance([0.0], [5.0], 1) == 5.0


def test_minkowski_distance_three_dimensions():
    result = minkowski_distance([1.0, 2.0, 3.0], [4.0, 6.0, 8.0], 2)
    expected = (9.0 + 16.0 + 25.0) ** 0.5
    assert abs(result - expected) < 1e-9


def test_minkowski_distance_order_1_multiple_dimensions():
    assert minkowski_distance([0.0, 0.0, 0.0], [1.0, 2.0, 3.0], 1) == 6.0


def test_minkowski_distance_fractional_values():
    result = minkowski_distance([0.5, 1.5], [2.5, 3.5], 2)
    expected = (4.0 + 4.0) ** 0.5
    assert abs(result - expected) < 1e-9


def test_minkowski_distance_order_less_than_1():
    with pytest.raises(ValueError, match="The order must be greater than or equal to 1."):
        minkowski_distance([1.0], [2.0], 0)


def test_minkowski_distance_negative_order():
    with pytest.raises(ValueError, match="The order must be greater than or equal to 1."):
        minkowski_distance([1.0], [2.0], -1)


def test_minkowski_distance_different_dimensions():
    with pytest.raises(ValueError, match="Both points must have the same dimension."):
        minkowski_distance([1.0], [1.0, 2.0], 1)


def test_minkowski_distance_different_dimensions_larger():
    with pytest.raises(ValueError, match="Both points must have the same dimension."):
        minkowski_distance([1.0, 2.0, 3.0], [1.0, 2.0], 2)


def test_minkowski_distance_empty_lists():
    assert minkowski_distance([], [], 1) == 0.0


def test_minkowski_distance_large_order():
    result = minkowski_distance([1.0, 1.0], [2.0, 2.0], 100)
    assert abs(result - 1.0) < 0.01