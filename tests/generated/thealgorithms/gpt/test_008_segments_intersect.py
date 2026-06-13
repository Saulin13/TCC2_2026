import pytest
from geometry.segment_intersection import segments_intersect
from geometry.point import Point

def test_segments_intersect_proper_intersection():
    assert segments_intersect(Point(0, 0), Point(2, 2), Point(0, 2), Point(2, 0)) is True

def test_segments_intersect_collinear_overlap():
    assert segments_intersect(Point(0, 0), Point(2, 2), Point(1, 1), Point(3, 3)) is True

def test_segments_intersect_no_intersection_parallel():
    assert segments_intersect(Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0)) is False

def test_segments_intersect_no_intersection_non_parallel():
    assert segments_intersect(Point(0, 0), Point(1, 1), Point(1, 0), Point(2, 1)) is False

def test_segments_intersect_no_intersection_vertical():
    assert segments_intersect(Point(0, 0), Point(1, 1), Point(0, 1), Point(0, 2)) is False

def test_segments_intersect_endpoint_on_segment():
    assert segments_intersect(Point(0, 0), Point(1, 0), Point(1, 0), Point(2, 0)) is True

def test_segments_intersect_same_segment():
    assert segments_intersect(Point(0, 0), Point(1, 1), Point(0, 0), Point(1, 1)) is True

def test_segments_intersect_touching_at_endpoint():
    assert segments_intersect(Point(0, 0), Point(1, 1), Point(1, 1), Point(2, 2)) is True

def test_segments_intersect_no_intersection_touching_but_not_intersecting():
    assert segments_intersect(Point(0, 0), Point(1, 1), Point(2, 2), Point(3, 3)) is False

def test_segments_intersect_exception_invalid_input():
    with pytest.raises(TypeError):
        segments_intersect(Point(0, 0), Point(1, 1), "invalid", Point(2, 2))