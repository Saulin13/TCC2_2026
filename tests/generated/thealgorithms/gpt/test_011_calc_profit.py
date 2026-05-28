import pytest
from knapsack.greedy_knapsack import calc_profit

def test_calc_profit_normal_case():
    assert calc_profit([1, 2, 3], [3, 4, 5], 15) == 6
    assert calc_profit([10, 9, 8], [3, 4, 5], 25) == 27
    assert calc_profit([20, 30, 40], [5, 10, 15], 20) == 50

def test_calc_profit_edge_case():
    assert calc_profit([1, 2, 3], [3, 4, 5], 0) == 0
    assert calc_profit([1], [1], 1) == 1
    assert calc_profit([1], [1], 0) == 0

def test_calc_profit_max_weight_exceeded():
    assert calc_profit([10, 20, 30], [5, 10, 15], 5) == 10
    assert calc_profit([10, 20, 30], [5, 10, 15], 10) == 20
    assert calc_profit([10, 20, 30], [5, 10, 15], 15) == 30

def test_calc_profit_invalid_length():
    with pytest.raises(ValueError, match="The length of profit and weight must be same."):
        calc_profit([1, 2], [1], 10)

def test_calc_profit_negative_profit():
    with pytest.raises(ValueError, match="Profit can not be negative."):
        calc_profit([-1, 2, 3], [1, 2, 3], 10)

def test_calc_profit_negative_weight():
    with pytest.raises(ValueError, match="Weight can not be negative."):
        calc_profit([1, 2, 3], [-1, 2, 3], 10)

def test_calc_profit_zero_max_weight():
    with pytest.raises(ValueError, match="max_weight must greater than zero."):
        calc_profit([1, 2, 3], [1, 2, 3], 0)