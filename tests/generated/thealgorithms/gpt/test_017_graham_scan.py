import pytest
from other.graham_scan import graham_scan

def test_graham_scan_normal_case():
    points = [(9, 6), (3, 1), (0, 0), (5, 5), (5, 2), (7, 0), (3, 3), (1, 4)]
    expected = [(0, 0), (7, 0), (9, 6), (5, 5), (1, 4)]
    assert graham_scan(points) == expected

def test_graham_scan_square():
    points = [(0, 0), (1, 0), (1, 1), (0, 1)]
    expected = [(0, 0), (1, 0), (1, 1), (0, 1)]
    assert graham_scan(points) == expected

def test_graham_scan_collinear_points():
    points = [(0, 0), (1, 1), (2, 2), (3, 3), (-1, 2)]
    expected = [(0, 0), (1, 1), (2, 2), (3, 3), (-1, 2)]
    assert graham_scan(points) == expected

def test_graham_scan_large_coordinates():
    points = [(-100, 20), (99, 3), (1, 10000001), (5133186, -25), (-66, -4)]
    expected = [(5133186, -25), (1, 10000001), (-100, 20), (-66, -4)]
    assert graham_scan(points) == expected

def test_graham_scan_minimum_points():
    points = [(0, 0), (1, 1), (2, 2)]
    expected = [(0, 0), (1, 1), (2, 2)]
    assert graham_scan(points) == expected

def test_graham_scan_insufficient_points():
    with pytest.raises(ValueError, match="graham_scan: argument must contain more than 3 points."):
        graham_scan([(0, 0), (1, 1)])