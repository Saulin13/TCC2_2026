import pytest
from knapsack.greedy_knapsack import calc_profit

def test_calc_profit_normal_case():
    assert calc_profit([1, 2, 3], [3, 4, 5], 15) == 6
    assert calc_profit([10, 9, 8], [3, 4, 5], 25) == 27

def test_calc_profit_edge_case_zero_max_weight():
    with pytest.raises(ValueError, match="max_weight must greater than zero."):
        calc_profit([1, 2, 3], [3, 4, 5], 0)

def test_calc_profit_edge_case_negative_max_weight():
    with pytest.raises(ValueError, match="max_weight must greater than zero."):
        calc_profit([1, 2, 3], [3, 4, 5], -5)

def test_calc_profit_edge_case_empty_lists():
    assert calc_profit([], [], 10) == 0

def test_calc_profit_edge_case_single_item():
    assert calc_profit([5], [5], 5) == 5
    assert calc_profit([5], [5], 10) == 5

def test_calc_profit_exception_mismatched_lengths():
    with pytest.raises(ValueError, match="The length of profit and weight must be same."):
        calc_profit([1, 2], [3], 10)

def test_calc_profit_exception_negative_profit():
    with pytest.raises(ValueError, match="Profit can not be negative."):
        calc_profit([-1, 2, 3], [3, 4, 5], 10)

def test_calc_profit_exception_negative_weight():
    with pytest.raises(ValueError, match="Weight can not be negative."):
        calc_profit([1, 2, 3], [3, -4, 5], 10)

def test_calc_profit_partial_fill():
    assert calc_profit([10, 5, 15], [2, 3, 5], 5) == 25  # Choose items with profit 10 and 15