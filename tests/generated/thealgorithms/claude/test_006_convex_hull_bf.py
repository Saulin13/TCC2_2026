import pytest
from divide_and_conquer.convex_hull import convex_hull_bf


def test_convex_hull_bf_triangle():
    points = [[0, 0], [1, 0], [10, 1]]
    result = convex_hull_bf(points)
    expected = [(0.0, 0.0), (1.0, 0.0), (10.0, 1.0)]
    assert result == expected


def test_convex_hull_bf_collinear_points():
    points = [[0, 0], [1, 0], [10, 0]]
    result = convex_hull_bf(points)
    expected = [(0.0, 0.0), (10.0, 0.0)]
    assert result == expected


def test_convex_hull_bf_square_with_interior_points():
    points = [[-1, 1], [-1, -1], [0, 0], [0.5, 0.5], [1, -1], [1, 1], [-0.75, 1]]
    result = convex_hull_bf(points)
    expected = [(-1.0, -1.0), (-1.0, 1.0), (1.0, -1.0), (1.0, 1.0)]
    assert result == expected


def test_convex_hull_bf_complex_set():
    points = [(0, 3), (2, 2), (1, 1), (2, 1), (3, 0), (0, 0), (3, 3), (2, -1), (2, -4), (1, -3)]
    result = convex_hull_bf(points)
    expected = [(0.0, 0.0), (0.0, 3.0), (1.0, -3.0), (2.0, -4.0), (3.0, 0.0), (3.0, 3.0)]
    assert result == expected


def test_convex_hull_bf_single_point():
    points = [[5, 5]]
    result = convex_hull_bf(points)
    expected = [(5.0, 5.0)]
    assert result == expected


def test_convex_hull_bf_two_points():
    points = [[0, 0], [1, 1]]
    result = convex_hull_bf(points)
    expected = [(0.0, 0.0), (1.0, 1.0)]
    assert result == expected


def test_convex_hull_bf_duplicate_points():
    points = [[0, 0], [0, 0], [1, 1], [1, 1]]
    result = convex_hull_bf(points)
    expected = [(0.0, 0.0), (1.0, 1.0)]
    assert result == expected


def test_convex_hull_bf_pentagon():
    points = [[0, 0], [2, 0], [3, 2], [1, 3], [-1, 2]]
    result = convex_hull_bf(points)
    expected = [(-1.0, 2.0), (0.0, 0.0), (1.0, 3.0), (2.0, 0.0), (3.0, 2.0)]
    assert result == expected


def test_convex_hull_bf_negative_coordinates():
    points = [[-5, -5], [-3, -2], [-1, -4], [0, 0]]
    result = convex_hull_bf(points)
    expected = [(-5.0, -5.0), (-3.0, -2.0), (-1.0, -4.0), (0.0, 0.0)]
    assert result == expected


def test_convex_hull_bf_tuples_input():
    points = [(0, 0), (1, 0), (0.5, 1)]
    result = convex_hull_bf(points)
    expected = [(0.0, 0.0), (0.5, 1.0), (1.0, 0.0)]
    assert result == expected


def test_convex_hull_bf_floating_point():
    points = [[0.5, 0.5], [1.5, 1.5], [2.5, 0.5], [1.5, -0.5]]
    result = convex_hull_bf(points)
    expected = [(0.5, 0.5), (1.5, -0.5), (1.5, 1.5), (2.5, 0.5)]
    assert result == expected


def test_convex_hull_bf_empty_list():
    points = []
    result = convex_hull_bf(points)
    expected = []
    assert result == expected


def test_convex_hull_bf_all_collinear_vertical():
    points = [[1, 0], [1, 1], [1, 2], [1, 3]]
    result = convex_hull_bf(points)
    expected = [(1.0, 0.0), (1.0, 3.0)]
    assert result == expected


def test_convex_hull_bf_all_collinear_horizontal():
    points = [[0, 1], [1, 1], [2, 1], [3, 1]]
    result = convex_hull_bf(points)
    expected = [(0.0, 1.0), (3.0, 1.0)]
    assert result == expected