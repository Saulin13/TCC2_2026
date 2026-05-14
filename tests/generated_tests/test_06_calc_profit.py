import sys
import os
sys.path.append(r'C:\Users\diogo\OneDrive\Área de Trabalho\Diogo\PUC\8 Periodo\TCC\TCC2_2026/repos/Python')
from knapsack.greedy_knapsack import calc_profit
import os
import sys




import pytest

def test_calc_profit():
    # Test cases from the docstring
    assert calc_profit([1, 2, 3], [3, 4, 5], 15) == 6
    assert calc_profit([10, 9, 8], [3, 4, 5], 25) == 27

    # Additional test cases
    assert calc_profit([60, 100, 120], [10, 20, 30], 50) == 240
    assert calc_profit([10, 20, 30], [5, 10, 15], 10) == 20
    assert calc_profit([10, 20, 30], [5, 10, 15], 0) == 0

    # Test with zero max_weight
    with pytest.raises(ValueError, match="max_weight must greater than zero."):
        calc_profit([10, 20, 30], [5, 10, 15], 0)

    # Test with negative profit
    with pytest.raises(ValueError, match="Profit can not be negative."):
        calc_profit([-10, 20, 30], [5, 10, 15], 50)

    # Test with negative weight
    with pytest.raises(ValueError, match="Weight can not be negative."):
        calc_profit([10, 20, 30], [5, -10, 15], 50)

    # Test with different lengths of profit and weight
    with pytest.raises(ValueError, match="The length of profit and weight must be same."):
        calc_profit([10, 20], [5, 10, 15], 50)
