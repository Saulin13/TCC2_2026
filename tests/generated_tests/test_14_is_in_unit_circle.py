import sys
import os
sys.path.append(r'C:\Users\diogo\OneDrive\Área de Trabalho\Diogo\PUC\8 Periodo\TCC\TCC2_2026/repos/Python')
from maths.pi_monte_carlo_estimation import is_in_unit_circle
import os
import sys




import pytest

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_in_unit_circle(self) -> bool:
        """
        True, if the point lies in the unit circle
        False, otherwise
        """
        return (self.x**2 + self.y**2) <= 1

def test_is_in_unit_circle():
    # Test point inside the unit circle
    point_inside = Point(0.5, 0.5)
    assert point_inside.is_in_unit_circle() == True

    # Test point on the boundary of the unit circle
    point_on_boundary = Point(1, 0)
    assert point_on_boundary.is_in_unit_circle() == True

    # Test point outside the unit circle
    point_outside = Point(1, 1)
    assert point_outside.is_in_unit_circle() == False

    # Test point at the origin
    point_origin = Point(0, 0)
    assert point_origin.is_in_unit_circle() == True

    # Test point on the negative x-axis
    point_negative_x = Point(-1, 0)
    assert point_negative_x.is_in_unit_circle() == True

    # Test point on the negative y-axis
    point_negative_y = Point(0, -1)
    assert point_negative_y.is_in_unit_circle() == True
