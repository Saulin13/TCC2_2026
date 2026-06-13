import pytest
from maths.area import area_triangle_three_sides

def test_area_triangle_three_sides_normal_cases():
    assert area_triangle_three_sides(5, 12, 13) == 30.0
    assert area_triangle_three_sides(10, 11, 12) == pytest.approx(51.521233486786784)
    assert area_triangle_three_sides(1.6, 2.6, 3.6) == pytest.approx(1.8703742940919619)

def test_area_triangle_three_sides_edge_cases():
    assert area_triangle_three_sides(0, 0, 0) == 0.0

def test_area_triangle_three_sides_invalid_negative_sides():
    with pytest.raises(ValueError, match="area_triangle_three_sides() only accepts non-negative values"):
        area_triangle_three_sides(-1, -2, -1)
    with pytest.raises(ValueError, match="area_triangle_three_sides() only accepts non-negative values"):
        area_triangle_three_sides(1, -2, 1)

def test_area_triangle_three_sides_invalid_non_triangle():
    with pytest.raises(ValueError, match="Given three sides do not form a triangle"):
        area_triangle_three_sides(2, 4, 7)
    with pytest.raises(ValueError, match="Given three sides do not form a triangle"):
        area_triangle_three_sides(2, 7, 4)
    with pytest.raises(ValueError, match="Given three sides do not form a triangle"):
        area_triangle_three_sides(7, 2, 4)