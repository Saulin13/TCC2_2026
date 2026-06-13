import pytest
from maths.minkowski_distance import minkowski_distance

def test_minkowski_distance_normal_cases():
    assert minkowski_distance([1.0, 1.0], [2.0, 2.0], 1) == 2.0
    assert minkowski_distance([1.0, 2.0, 3.0, 4.0], [5.0, 6.0, 7.0, 8.0], 2) == 8.0
    assert pytest.approx(minkowski_distance([5.0], [0.0], 3), 0.0001) == 5.0

def test_minkowski_distance_edge_cases():
    assert minkowski_distance([0.0], [0.0], 1) == 0.0
    assert minkowski_distance([0.0, 0.0], [0.0, 0.0], 2) == 0.0
    assert minkowski_distance([1.0], [1.0], 1) == 0.0

def test_minkowski_distance_invalid_order():
    with pytest.raises(ValueError, match="The order must be greater than or equal to 1."):
        minkowski_distance([1.0], [2.0], -1)

def test_minkowski_distance_dimension_mismatch():
    with pytest.raises(ValueError, match="Both points must have the same dimension."):
        minkowski_distance([1.0], [1.0, 2.0], 1)