import sys
import os
sys.path.append(r'C:\Users\diogo\OneDrive\Área de Trabalho\Diogo\PUC\8 Periodo\TCC\TCC2_2026/repos/Python')
from data_structures.arrays.kth_largest_element import kth_largest_element
import os
import sys




import pytest

def test_kth_largest_element():
    # Test cases with valid inputs
    assert kth_largest_element([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5], 3) == 5
    assert kth_largest_element([2, 5, 6, 1, 9, 3, 8, 4, 7, 3, 5], 1) == 9
    assert kth_largest_element(['apple', 'cherry', 'date', 'banana'], 2) == 'cherry'
    assert kth_largest_element([3.1, 1.2, 5.6, 4.7, 7.9, 5, 0], 2) == 5.6
    assert kth_largest_element([-2, -5, -4, -1], 1) == -1

    # Test cases with invalid inputs
    with pytest.raises(ValueError, match="Invalid value of 'position'"):
        kth_largest_element([2, 5, 6, 1, 9, 3, 8, 4, 7, 3, 5], -2)
    with pytest.raises(ValueError, match="Invalid value of 'position'"):
        kth_largest_element([9, 1, 3, 6, 7, 9, 8, 4, 2, 4, 9], 110)
    with pytest.raises(ValueError, match="Invalid value of 'position'"):
        kth_largest_element([1, 2, 4, 3, 5, 9, 7, 6, 5, 9, 3], 0)
    with pytest.raises(ValueError, match="The position should be an integer"):
        kth_largest_element([3.1, 1.2, 5.6, 4.7, 7.9, 5, 0], 1.5)
    with pytest.raises(TypeError, match="'tuple' object does not support item assignment"):
        kth_largest_element((4, 6, 1, 2), 4)

    # Test case with an empty list
    assert kth_largest_element([], 1) == -1
