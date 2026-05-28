import pytest
from geometry.segment_intersection import segments_intersect
from geometry.point import Point


class TestSegmentsIntersect:
    """Test suite for segments_intersect function."""

    # Normal cases - segments that intersect
    def test_crossing_segments(self):
        """Test two segments that cross each other."""
        assert segments_intersect(
            Point(0, 0), Point(2, 2), Point(0, 2), Point(2, 0)
        ) is True

    def test_overlapping_collinear_segments(self):
        """Test collinear segments that overlap."""
        assert segments_intersect(
            Point(0, 0), Point(2, 2), Point(1, 1), Point(3, 3)
        ) is True

    def test_touching_at_endpoint(self):
        """Test segments that touch at exactly one endpoint."""
        assert segments_intersect(
            Point(0, 0), Point(1, 0), Point(1, 0), Point(2, 0)
        ) is True

    def test_t_intersection(self):
        """Test T-shaped intersection where one endpoint touches the other segment."""
        assert segments_intersect(
            Point(0, 0), Point(4, 0), Point(2, -1), Point(2, 1)
        ) is True

    def test_vertical_and_horizontal_intersection(self):
        """Test vertical and horizontal segments intersecting."""
        assert segments_intersect(
            Point(1, 0), Point(1, 4), Point(0, 2), Point(3, 2)
        ) is True

    # Normal cases - segments that do not intersect
    def test_non_intersecting_parallel_segments(self):
        """Test parallel segments that don't intersect."""
        assert segments_intersect(
            Point(0, 0), Point(1, 1), Point(1, 0), Point(2, 1)
        ) is False

    def test_non_intersecting_perpendicular_segments(self):
        """Test perpendicular segments that don't intersect."""
        assert segments_intersect(
            Point(0, 0), Point(1, 1), Point(0, 1), Point(0, 2)
        ) is False

    def test_collinear_non_overlapping_segments(self):
        """Test collinear segments that don't overlap."""
        assert segments_intersect(
            Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0)
        ) is False

    def test_segments_far_apart(self):
        """Test segments that are far apart."""
        assert segments_intersect(
            Point(0, 0), Point(1, 1), Point(10, 10), Point(11, 11)
        ) is False

    # Edge cases
    def test_point_segments_same_location(self):
        """Test two point segments at the same location."""
        assert segments_intersect(
            Point(1, 1), Point(1, 1), Point(1, 1), Point(1, 1)
        ) is True

    def test_point_segment_on_line_segment(self):
        """Test a point segment lying on a line segment."""
        assert segments_intersect(
            Point(0, 0), Point(2, 2), Point(1, 1), Point(1, 1)
        ) is True

    def test_point_segment_not_on_line_segment(self):
        """Test a point segment not on a line segment."""
        assert segments_intersect(
            Point(0, 0), Point(2, 2), Point(1, 0), Point(1, 0)
        ) is False

    def test_shared_endpoint(self):
        """Test segments sharing exactly one endpoint."""
        assert segments_intersect(
            Point(0, 0), Point(1, 1), Point(1, 1), Point(2, 0)
        ) is True

    def test_negative_coordinates(self):
        """Test segments with negative coordinates."""
        assert segments_intersect(
            Point(-2, -2), Point(2, 2), Point(-2, 2), Point(2, -2)
        ) is True

    def test_floating_point_coordinates(self):
        """Test segments with floating point coordinates."""
        assert segments_intersect(
            Point(0.5, 0.5), Point(2.5, 2.5), Point(0.5, 2.5), Point(2.5, 0.5)
        ) is True

    def test_horizontal_segments_different_y(self):
        """Test horizontal segments at different y-coordinates."""
        assert segments_intersect(
            Point(0, 0), Point(2, 0), Point(0, 1), Point(2, 1)
        ) is False

    def test_vertical_segments_different_x(self):
        """Test vertical segments at different x-coordinates."""
        assert segments_intersect(
            Point(0, 0), Point(0, 2), Point(1, 0), Point(1, 2)
        ) is False

    def test_almost_touching_segments(self):
        """Test segments that are very close but don't touch."""
        assert segments_intersect(
            Point(0, 0), Point(1, 0), Point(1.001, 0), Point(2, 0)
        ) is False

    def test_cross_at_origin(self):
        """Test segments crossing at origin."""
        assert segments_intersect(
            Point(-1, 0), Point(1, 0), Point(0, -1), Point(0, 1)
        ) is True

    # Exception/failure path
    def test_invalid_point_type(self):
        """Test that function raises error with invalid point types."""
        with pytest.raises(AttributeError):
            segments_intersect((0, 0), Point(1, 1), Point(0, 1), Point(1, 0))

    def test_none_as_point(self):
        """Test that function raises error when None is passed as point."""
        with pytest.raises(AttributeError):
            segments_intersect(None, Point(1, 1), Point(0, 1), Point(1, 0))