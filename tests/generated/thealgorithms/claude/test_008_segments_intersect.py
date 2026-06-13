import pytest
from geometry.segment_intersection import segments_intersect
from geometry.point import Point


class TestSegmentsIntersect:
    """Test suite for segments_intersect function."""

    def test_segments_cross_at_center(self):
        """Test two segments that properly cross in the middle."""
        p1 = Point(0, 0)
        p2 = Point(2, 2)
        p3 = Point(0, 2)
        p4 = Point(2, 0)
        assert segments_intersect(p1, p2, p3, p4) is True

    def test_segments_overlap_collinear(self):
        """Test two collinear segments that overlap."""
        p1 = Point(0, 0)
        p2 = Point(2, 2)
        p3 = Point(1, 1)
        p4 = Point(3, 3)
        assert segments_intersect(p1, p2, p3, p4) is True

    def test_segments_collinear_no_overlap(self):
        """Test two collinear segments that don't overlap."""
        p1 = Point(0, 0)
        p2 = Point(1, 0)
        p3 = Point(2, 0)
        p4 = Point(3, 0)
        assert segments_intersect(p1, p2, p3, p4) is False

    def test_segments_parallel_no_intersection(self):
        """Test two parallel segments that don't intersect."""
        p1 = Point(0, 0)
        p2 = Point(1, 1)
        p3 = Point(1, 0)
        p4 = Point(2, 1)
        assert segments_intersect(p1, p2, p3, p4) is False

    def test_segments_perpendicular_no_intersection(self):
        """Test two perpendicular segments that don't intersect."""
        p1 = Point(0, 0)
        p2 = Point(1, 1)
        p3 = Point(0, 1)
        p4 = Point(0, 2)
        assert segments_intersect(p1, p2, p3, p4) is False

    def test_segments_share_endpoint(self):
        """Test two segments that share an endpoint."""
        p1 = Point(0, 0)
        p2 = Point(1, 0)
        p3 = Point(1, 0)
        p4 = Point(2, 0)
        assert segments_intersect(p1, p2, p3, p4) is True

    def test_segments_t_intersection(self):
        """Test T-shaped intersection where one endpoint touches the other segment."""
        p1 = Point(0, 0)
        p2 = Point(4, 0)
        p3 = Point(2, 0)
        p4 = Point(2, 2)
        assert segments_intersect(p1, p2, p3, p4) is True

    def test_segments_cross_negative_coordinates(self):
        """Test segments crossing with negative coordinates."""
        p1 = Point(-2, -2)
        p2 = Point(2, 2)
        p3 = Point(-2, 2)
        p4 = Point(2, -2)
        assert segments_intersect(p1, p2, p3, p4) is True

    def test_segments_horizontal_vertical_cross(self):
        """Test horizontal and vertical segments that cross."""
        p1 = Point(0, 1)
        p2 = Point(4, 1)
        p3 = Point(2, 0)
        p4 = Point(2, 3)
        assert segments_intersect(p1, p2, p3, p4) is True

    def test_segments_horizontal_vertical_no_cross(self):
        """Test horizontal and vertical segments that don't cross."""
        p1 = Point(0, 0)
        p2 = Point(2, 0)
        p3 = Point(3, -1)
        p4 = Point(3, 1)
        assert segments_intersect(p1, p2, p3, p4) is False

    def test_segments_same_segment(self):
        """Test a segment with itself."""
        p1 = Point(0, 0)
        p2 = Point(1, 1)
        p3 = Point(0, 0)
        p4 = Point(1, 1)
        assert segments_intersect(p1, p2, p3, p4) is True

    def test_segments_point_on_segment(self):
        """Test where one segment is a point on the other segment."""
        p1 = Point(0, 0)
        p2 = Point(4, 4)
        p3 = Point(2, 2)
        p4 = Point(2, 2)
        assert segments_intersect(p1, p2, p3, p4) is True

    def test_segments_almost_touching(self):
        """Test segments that are very close but don't touch."""
        p1 = Point(0, 0)
        p2 = Point(1, 0)
        p3 = Point(1.001, 0)
        p4 = Point(2, 0)
        assert segments_intersect(p1, p2, p3, p4) is False

    def test_segments_x_shape(self):
        """Test segments forming an X shape."""
        p1 = Point(1, 1)
        p2 = Point(3, 3)
        p3 = Point(1, 3)
        p4 = Point(3, 1)
        assert segments_intersect(p1, p2, p3, p4) is True

    def test_segments_endpoint_touches_other_endpoint(self):
        """Test where endpoints of both segments touch."""
        p1 = Point(0, 0)
        p2 = Point(1, 1)
        p3 = Point(1, 1)
        p4 = Point(2, 2)
        assert segments_intersect(p1, p2, p3, p4) is True

    def test_segments_floating_point_coordinates(self):
        """Test segments with floating point coordinates."""
        p1 = Point(0.5, 0.5)
        p2 = Point(2.5, 2.5)
        p3 = Point(0.5, 2.5)
        p4 = Point(2.5, 0.5)
        assert segments_intersect(p1, p2, p3, p4) is True

    def test_segments_zero_length(self):
        """Test where both segments are zero-length (points) at same location."""
        p1 = Point(1, 1)
        p2 = Point(1, 1)
        p3 = Point(1, 1)
        p4 = Point(1, 1)
        assert segments_intersect(p1, p2, p3, p4) is True

    def test_segments_zero_length_different_points(self):
        """Test where both segments are zero-length (points) at different locations."""
        p1 = Point(0, 0)
        p2 = Point(0, 0)
        p3 = Point(1, 1)
        p4 = Point(1, 1)
        assert segments_intersect(p1, p2, p3, p4) is False