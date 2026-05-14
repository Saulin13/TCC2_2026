import sys
import os
sys.path.append(r'C:\Users\diogo\OneDrive\Área de Trabalho\Diogo\PUC\8 Periodo\TCC\TCC2_2026/repos/Python')
from maths.series.geometric import is_geometric_series
import os
import sys




import pytest

def test_is_geometric_series():
    # Test cases where the series is geometric
    assert is_geometric_series([2, 4, 8]) == True
    assert is_geometric_series([3, 6, 12, 24]) == True
    assert is_geometric_series([5]) == True  # Single element is considered geometric

    # Test cases where the series is not geometric
    assert is_geometric_series([1, 2, 3]) == False
    assert is_geometric_series([0, 0, 3]) == False

    # Test cases for invalid inputs
    with pytest.raises(ValueError, match="Input list must be a non empty list"):
        is_geometric_series([])

    with pytest.raises(ValueError, match="Input series is not valid, valid series - [2, 4, 8]"):
        is_geometric_series(4)

    # Test case with zero division
    assert is_geometric_series([0, 0, 0]) == True  # All zeros are considered geometric
    assert is_geometric_series([0, 0, 1]) == False
