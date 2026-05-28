import pytest
from maths.area import area_triangle_three_sides


def test_area_triangle_three_sides_right_triangle():
    assert area_triangle_three_sides(5, 12, 13) == 30.0


def test_area_triangle_three_sides_regular_triangle():
    result = area_triangle_three_sides(10, 11, 12)
    assert abs(result - 51.521233486786784) < 1e-10


def test_area_triangle_three_sides_zero_sides():
    assert area_triangle_three_sides(0, 0, 0) == 0.0


def test_area_triangle_three_sides_float_values():
    result = area_triangle_three_sides(1.6, 2.6, 3.6)
    assert abs(result - 1.8703742940919619) < 1e-10


def test_area_triangle_three_sides_equilateral():
    result = area_triangle_three_sides(3, 3, 3)
    expected = 3.897114317029974
    assert abs(result - expected) < 1e-10


def test_area_triangle_three_sides_isosceles():
    result = area_triangle_three_sides(5, 5, 6)
    expected = 12.0
    assert abs(result - expected) < 1e-10


def test_area_triangle_three_sides_large_values():
    result = area_triangle_three_sides(100, 150, 200)
    assert result > 0


def test_area_triangle_three_sides_all_negative():
    with pytest.raises(ValueError, match="area_triangle_three_sides\\(\\) only accepts non-negative values"):
        area_triangle_three_sides(-1, -2, -1)


def test_area_triangle_three_sides_one_negative():
    with pytest.raises(ValueError, match="area_triangle_three_sides\\(\\) only accepts non-negative values"):
        area_triangle_three_sides(1, -2, 1)


def test_area_triangle_three_sides_first_negative():
    with pytest.raises(ValueError, match="area_triangle_three_sides\\(\\) only accepts non-negative values"):
        area_triangle_three_sides(-5, 12, 13)


def test_area_triangle_three_sides_invalid_triangle_case1():
    with pytest.raises(ValueError, match="Given three sides do not form a triangle"):
        area_triangle_three_sides(2, 4, 7)


def test_area_triangle_three_sides_invalid_triangle_case2():
    with pytest.raises(ValueError, match="Given three sides do not form a triangle"):
        area_triangle_three_sides(2, 7, 4)


def test_area_triangle_three_sides_invalid_triangle_case3():
    with pytest.raises(ValueError, match="Given three sides do not form a triangle"):
        area_triangle_three_sides(7, 2, 4)


def test_area_triangle_three_sides_invalid_triangle_equal_sum():
    with pytest.raises(ValueError, match="Given three sides do not form a triangle"):
        area_triangle_three_sides(1, 2, 3)


def test_area_triangle_three_sides_very_small_triangle():
    result = area_triangle_three_sides(0.1, 0.1, 0.1)
    assert result > 0
    assert result < 0.01
```