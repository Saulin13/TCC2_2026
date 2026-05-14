import sys
import os
sys.path.append(r'C:\Users\diogo\OneDrive\Área de Trabalho\Diogo\PUC\8 Periodo\TCC\TCC2_2026/repos/Python')
from divide_and_conquer.convex_hull import convex_hull_bf
import os
import sys




import pytest
from collections import namedtuple

# Define a simple Point class for testing
Point = namedtuple('Point', ['x', 'y'])

# Assuming _validate_input and _det are defined elsewhere in the module
def _validate_input(points):
    return [Point(float(p[0]), float(p[1])) for p in points]

def _det(p1, p2, p3):
    return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)

def test_convex_hull_bf():
    # Test case 1: Simple triangle
    points = [Point(0, 0), Point(1, 0), Point(10, 1)]
    expected = [Point(0.0, 0.0), Point(1.0, 0.0), Point(10.0, 1.0)]
    assert convex_hull_bf(points) == expected

    # Test case 2: Collinear points
    points = [Point(0, 0), Point(1, 0), Point(10, 0)]
    expected = [Point(0.0, 0.0), Point(10.0, 0.0)]
    assert convex_hull_bf(points) == expected

    # Test case 3: Points forming a square
    points = [Point(-1, 1), Point(-1, -1), Point(0, 0), Point(0.5, 0.5), Point(1, -1), Point(1, 1), Point(-0.75, 1)]
    expected = [Point(-1.0, -1.0), Point(-1.0, 1.0), Point(1.0, -1.0), Point(1.0, 1.0)]
    assert convex_hull_bf(points) == expected

    # Test case 4: Complex shape
    points = [Point(0, 3), Point(2, 2), Point(1, 1), Point(2, 1), Point(3, 0), Point(0, 0), Point(3, 3), Point(2, -1), Point(2, -4), Point(1, -3)]
    expected = [Point(0.0, 0.0), Point(0.0, 3.0), Point(1.0, -3.0), Point(2.0, -4.0), Point(3.0, 0.0), Point(3.0, 3.0)]
    assert convex_hull_bf(points) == expected

    # Test case 5: Single point
    points = [Point(0, 0)]
    expected = [Point(0.0, 0.0)]
    assert convex_hull_bf(points) == expected

    # Test case 6: Two points
    points = [Point(0, 0), Point(1, 1)]
    expected = [Point(0.0, 0.0), Point(1.0, 1.0)]
    assert convex_hull_bf(points) == expected

    # Test case 7: No points
    points = []
    expected = []
    assert convex_hull_bf(points) == expected

