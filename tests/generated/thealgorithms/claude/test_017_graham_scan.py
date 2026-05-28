import pytest
from collections import deque
from other.graham_scan import graham_scan


def test_graham_scan_basic_octagon():
    points = [(9, 6), (3, 1), (0, 0), (5, 5), (5, 2), (7, 0), (3, 3), (1, 4)]
    result = graham_scan(points)
    assert result == [(0, 0), (7, 0), (9, 6), (5, 5), (1, 4)]


def test_graham_scan_square():
    points = [(0, 0), (1, 0), (1, 1), (0, 1)]
    result = graham_scan(points)
    assert result == [(0, 0), (1, 0), (1, 1), (0, 1)]


def test_graham_scan_collinear_points():
    points = [(0, 0), (1, 1), (2, 2), (3, 3), (-1, 2)]
    result = graham_scan(points)
    assert result == [(0, 0), (1, 1), (2, 2), (3, 3), (-1, 2)]


def test_graham_scan_large_coordinates():
    points = [(-100, 20), (99, 3), (1, 10000001), (5133186, -25), (-66, -4)]
    result = graham_scan(points)
    assert result == [(5133186, -25), (1, 10000001), (-100, 20), (-66, -4)]


def test_graham_scan_exactly_three_points():
    points = [(0, 0), (1, 0), (0, 1)]
    result = graham_scan(points)
    assert result == [(0, 0), (1, 0), (0, 1)]


def test_graham_scan_triangle():
    points = [(0, 0), (4, 0), (2, 3)]
    result = graham_scan(points)
    assert result == [(0, 0), (4, 0), (2, 3)]


def test_graham_scan_pentagon():
    points = [(0, 0), (2, 0), (3, 2), (1, 4), (-1, 2)]
    result = graham_scan(points)
    assert len(result) >= 3
    assert (0, 0) in result
    assert (2, 0) in result


def test_graham_scan_with_interior_points():
    points = [(0, 0), (4, 0), (4, 4), (0, 4), (2, 2), (1, 1), (3, 3)]
    result = graham_scan(points)
    assert (0, 0) in result
    assert (4, 0) in result
    assert (4, 4) in result
    assert (0, 4) in result
    assert (2, 2) not in result or len(result) == len(points)


def test_graham_scan_negative_coordinates():
    points = [(-5, -5), (-3, -1), (0, 0), (3, -1), (5, -5)]
    result = graham_scan(points)
    assert (-5, -5) in result or (5, -5) in result
    assert len(result) >= 3


def test_graham_scan_horizontal_line():
    points = [(0, 0), (1, 0), (2, 0), (3, 0)]
    result = graham_scan(points)
    assert len(result) >= 3


def test_graham_scan_vertical_line():
    points = [(0, 0), (0, 1), (0, 2), (0, 3)]
    result = graham_scan(points)
    assert len(result) >= 3


def test_graham_scan_two_points_raises_error():
    points = [(0, 0), (1, 1)]
    with pytest.raises(ValueError, match="graham_scan: argument must contain more than 3 points."):
        graham_scan(points)


def test_graham_scan_one_point_raises_error():
    points = [(0, 0)]
    with pytest.raises(ValueError, match="graham_scan: argument must contain more than 3 points."):
        graham_scan(points)


def test_graham_scan_empty_list_raises_error():
    points = []
    with pytest.raises(ValueError, match="graham_scan: argument must contain more than 3 points."):
        graham_scan(points)


def test_graham_scan_rectangle():
    points = [(0, 0), (5, 0), (5, 3), (0, 3)]
    result = graham_scan(points)
    assert result == [(0, 0), (5, 0), (5, 3), (0, 3)]


def test_graham_scan_with_duplicate_lowest_y():
    points = [(0, 0), (1, 0), (2, 1), (1, 2), (0, 1)]
    result = graham_scan(points)
    assert (0, 0) in result
    assert len(result) >= 3


def test_graham_scan_star_shape():
    points = [(0, 3), (1, 1), (3, 0), (1, -1), (0, -3), (-1, -1), (-3, 0), (-1, 1)]
    result = graham_scan(points)
    assert len(result) >= 3
    assert (0, -3) in result or (-3, 0) in result or (3, 0) in result or (0, 3) in result