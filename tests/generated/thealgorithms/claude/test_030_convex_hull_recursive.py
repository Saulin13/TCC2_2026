import pytest
from divide_and_conquer.convex_hull import convex_hull_recursive


def test_convex_hull_recursive_triangle():
    points = [[0, 0], [1, 0], [10, 1]]
    result = convex_hull_recursive(points)
    expected = [(0.0, 0.0), (1.0, 0.0), (10.0, 1.0)]
    assert result == expected


def test_convex_hull_recursive_collinear_points():
    points = [[0, 0], [1, 0], [10, 0]]
    result = convex_hull_recursive(points)
    expected = [(0.0, 0.0), (10.0, 0.0)]
    assert result == expected


def test_convex_hull_recursive_square_with_interior_points():
    points = [[-1, 1], [-1, -1], [0, 0], [0.5, 0.5], [1, -1], [1, 1], [-0.75, 1]]
    result = convex_hull_recursive(points)
    expected = [(-1.0, -1.0), (-1.0, 1.0), (1.0, -1.0), (1.0, 1.0)]
    assert result == expected


def test_convex_hull_recursive_complex_set():
    points = [(0, 3), (2, 2), (1, 1), (2, 1), (3, 0), (0, 0), (3, 3),
              (2, -1), (2, -4), (1, -3)]
    result = convex_hull_recursive(points)
    expected = [(0.0, 0.0), (0.0, 3.0), (1.0, -3.0), (2.0, -4.0), (3.0, 0.0), (3.0, 3.0)]
    assert result == expected


def test_convex_hull_recursive_single_point():
    points = [[5, 5]]
    result = convex_hull_recursive(points)
    expected = [(5.0, 5.0)]
    assert result == expected


def test_convex_hull_recursive_two_points():
    points = [[0, 0], [1, 1]]
    result = convex_hull_recursive(points)
    expected = [(0.0, 0.0), (1.0, 1.0)]
    assert result == expected


def test_convex_hull_recursive_duplicate_points():
    points = [[0, 0], [1, 1], [1, 1], [2, 2]]
    result = convex_hull_recursive(points)
    expected = [(0.0, 0.0), (2.0, 2.0)]
    assert result == expected


def test_convex_hull_recursive_negative_coordinates():
    points = [[-5, -5], [-3, -2], [0, 0], [3, 2], [5, 5]]
    result = convex_hull_recursive(points)
    expected = [(-5.0, -5.0), (5.0, 5.0)]
    assert result == expected


def test_convex_hull_recursive_pentagon():
    points = [[0, 0], [2, 1], [3, 3], [1, 4], [-1, 2]]
    result = convex_hull_recursive(points)
    assert (0.0, 0.0) in result
    assert (3.0, 3.0) in result
    assert (1.0, 4.0) in result
    assert (-1.0, 2.0) in result


def test_convex_hull_recursive_all_same_point():
    points = [[1, 1], [1, 1], [1, 1]]
    result = convex_hull_recursive(points)
    expected = [(1.0, 1.0)]
    assert result == expected


def test_convex_hull_recursive_vertical_line():
    points = [[0, 0], [0, 1], [0, 2], [0, 3]]
    result = convex_hull_recursive(points)
    expected = [(0.0, 0.0), (0.0, 3.0)]
    assert result == expected


def test_convex_hull_recursive_horizontal_line():
    points = [[0, 0], [1, 0], [2, 0], [3, 0]]
    result = convex_hull_recursive(points)
    expected = [(0.0, 0.0), (3.0, 0.0)]
    assert result == expected


def test_convex_hull_recursive_empty_list():
    points = []
    with pytest.raises((ValueError, IndexError)):
        convex_hull_recursive(points)


def test_convex_hull_recursive_invalid_point_dimension():
    points = [[0, 0, 0], [1, 1, 1]]
    with pytest.raises((ValueError, TypeError, IndexError)):
        convex_hull_recursive(points)


def test_convex_hull_recursive_mixed_types():
    points = [(0, 0), [1, 1], (2, 2)]
    result = convex_hull_recursive(points)
    expected = [(0.0, 0.0), (2.0, 2.0)]
    assert result == expected