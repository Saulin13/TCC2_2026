import sys
import os
sys.path.append(r'C:\Users\diogo\OneDrive\Área de Trabalho\Diogo\PUC\8 Periodo\TCC\TCC2_2026/repos/Python')
from maths.check_polygon import check_polygon
import os
import sys




import pytest

def test_check_polygon_valid_triangle():
    assert check_polygon([6, 10, 5]) == True

def test_check_polygon_invalid_polygon():
    assert check_polygon([3, 7, 13, 2]) == False

def test_check_polygon_invalid_polygon_with_floats():
    assert check_polygon([1, 4.3, 5.2, 12.2]) == False

def test_check_polygon_no_reorder():
    nums = [3, 7, 13, 2]
    _ = check_polygon(nums)
    assert nums == [3, 7, 13, 2]

def test_check_polygon_empty_list():
    with pytest.raises(ValueError, match="Monogons and Digons are not polygons in the Euclidean space"):
        check_polygon([])

def test_check_polygon_negative_value():
    with pytest.raises(ValueError, match="All values must be greater than 0"):
        check_polygon([-2, 5, 6])
