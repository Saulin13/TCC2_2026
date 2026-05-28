import pytest
from divide_and_conquer.convex_hull import convex_hull_bf

def test_convex_hull_bf_normal_case():
    points = [(0, 0), (1, 0), (10, 1)]
    expected = [(0.0, 0.0), (1.0, 0.0), (10.0, 1.0)]
    assert convex_hull_bf(points) == expected

def test_convex_hull_bf_collinear_points():
    points = [(0, 0), (1, 0), (10, 0)]
    expected = [(0.0, 0.0), (10.0, 0.0)]
    assert convex_hull_bf(points) == expected

def test_convex_hull_bf_complex_case():
    points = [(-1, 1), (-1, -1), (0, 0), (0.5, 0.5), (1, -1), (1, 1), (-0.75, 1)]
    expected = [(-1.0, -1.0), (-1.0, 1.0), (1.0, -1.0), (1.0, 1.0)]
    assert convex_hull_bf(points) == expected

def test_convex_hull_bf_large_case():
    points = [(0, 3), (2, 2), (1, 1), (2, 1), (3, 0), (0, 0), (3, 3), (2, -1), (2, -4), (1, -3)]
    expected = [(0.0, 0.0), (0.0, 3.0), (1.0, -3.0), (2.0, -4.0), (3.0, 0.0), (3.0, 3.0)]
    assert convex_hull_bf(points) == expected

def test_convex_hull_bf_single_point():
    points = [(0, 0)]
    expected = [(0.0, 0.0)]
    assert convex_hull_bf(points) == expected

def test_convex_hull_bf_two_points():
    points = [(0, 0), (1, 1)]
    expected = [(0.0, 0.0), (1.0, 1.0)]
    assert convex_hull_bf(points) == expected

def test_convex_hull_bf_duplicate_points():
    points = [(0, 0), (1, 1), (1, 1), (0, 0)]
    expected = [(0.0, 0.0), (1.0, 1.0)]
    assert convex_hull_bf(points) == expected

def test_convex_hull_bf_no_points():
    points = []
    expected = []
    assert convex_hull_bf(points) == expected

def test_convex_hull_bf_invalid_input():
    with pytest.raises(TypeError):
        convex_hull_bf(None)