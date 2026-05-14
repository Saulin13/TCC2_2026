import pytest
from maths.area import area_ellipse
from math import pi

def test_area_ellipse_normal_cases():
    assert area_ellipse(10, 10) == pytest.approx(314.1592653589793)
    assert area_ellipse(10, 20) == pytest.approx(628.3185307179587)
    assert area_ellipse(1.6, 2.6) == pytest.approx(13.06902543893354)

def test_area_ellipse_edge_cases():
    assert area_ellipse(0, 0) == 0.0
    assert area_ellipse(0, 10) == 0.0
    assert area_ellipse(10, 0) == 0.0

def test_area_ellipse_negative_values():
    with pytest.raises(ValueError, match="area_ellipse() only accepts non-negative values"):
        area_ellipse(-10, 20)
    with pytest.raises(ValueError, match="area_ellipse() only accepts non-negative values"):
        area_ellipse(10, -20)
    with pytest.raises(ValueError, match="area_ellipse() only accepts non-negative values"):
        area_ellipse(-10, -20)