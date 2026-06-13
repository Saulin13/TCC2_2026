import pytest
from maths.area import area_triangle_three_sides


def test_area_triangle_three_sides_right_triangle():
    assert area_triangle_three_sides(5, 12, 13) == 30.0


def test_area_triangle_three_sides_scalene_triangle():
    result = area_triangle_three_sides(10, 11, 12)
    assert abs(result - 51.521233486786784) < 1e-10


def test_area_triangle_three_sides_equilateral_triangle():
    result = area_triangle_three_sides(6, 6, 6)
    expected = 15.588457268119896
    assert abs(result - expected) < 1e-10


def test_area_triangle_three_sides_isosceles_triangle():
    result = area_triangle_three_sides(5, 5, 8)
    expected = 12.0
    assert abs(result - expected) < 1e-10


def test_area_triangle_three_sides_zero_area():
    assert area_triangle_three_sides(0, 0, 0) == 0.0


def test_area_triangle_three_sides_float_values():
    result = area_triangle_three_sides(1.6, 2.6, 3.6)
    expected = 1.8703742940919619
    assert abs(result - expected) < 1e-10


def test_area_triangle_three_sides_small_triangle():
    result = area_triangle_three_sides(3, 4, 5)
    assert result == 6.0


def test_area_triangle_three_sides_large_triangle():
    result = area_triangle_three_sides(100, 150, 200)
    expected = 7261.843774138907
    assert abs(result - expected) < 1e-8


def test_area_triangle_three_sides_negative_first_side():
    with pytest.raises(ValueError, match="area_triangle_three_sides\\(\\) only accepts non-negative values"):
        area_triangle_three_sides(-1, 2, 3)


def test_area_triangle_three_sides_negative_second_side():
    with pytest.raises(ValueError, match="area_triangle_three_sides\\(\\) only accepts non-negative values"):
        area_triangle_three_sides(1, -2, 3)


def test_area_triangle_three_sides_negative_third_side():
    with pytest.raises(ValueError, match="area_triangle_three_sides\\(\\) only accepts non-negative values"):
        area_triangle_three_sides(1, 2, -3)


def test_area_triangle_three_sides_all_negative():
    with pytest.raises(ValueError, match="area_triangle_three_sides\\(\\) only accepts non-negative values"):
        area_triangle_three_sides(-1, -2, -1)


def test_area_triangle_three_sides_invalid_triangle_sum_first_two():
    with pytest.raises(ValueError, match="Given three sides do not form a triangle"):
        area_triangle_three_sides(2, 4, 7)


def test_area_triangle_three_sides_invalid_triangle_sum_first_third():
    with pytest.raises(ValueError, match="Given three sides do not form a triangle"):
        area_triangle_three_sides(2, 7, 4)


def test_area_triangle_three_sides_invalid_triangle_sum_second_third():
    with pytest.raises(ValueError, match="Given three sides do not form a triangle"):
        area_triangle_three_sides(7, 2, 4)


def test_area_triangle_three_sides_degenerate_triangle():
    with pytest.raises(ValueError, match="Given three sides do not form a triangle"):
        area_triangle_three_sides(1, 2, 3)


def test_area_triangle_three_sides_one_zero_side():
    with pytest.raises(ValueError, match="Given three sides do not form a triangle"):
        area_triangle_three_sides(0, 5, 5)