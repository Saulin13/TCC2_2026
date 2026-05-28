import pytest
from knapsack.greedy_knapsack import calc_profit


def test_calc_profit_basic_case_1():
    result = calc_profit([1, 2, 3], [3, 4, 5], 15)
    assert result == 6


def test_calc_profit_basic_case_2():
    result = calc_profit([10, 9, 8], [3, 4, 5], 25)
    assert result == 27


def test_calc_profit_single_item_fits():
    result = calc_profit([10], [5], 10)
    assert result == 10


def test_calc_profit_single_item_partial():
    result = calc_profit([10], [5], 3)
    assert result == 6


def test_calc_profit_no_weight_capacity():
    result = calc_profit([10, 20, 30], [5, 10, 15], 0)
    assert result == 0


def test_calc_profit_all_items_fit():
    result = calc_profit([60, 100, 120], [10, 20, 30], 100)
    assert result == 280


def test_calc_profit_fractional_knapsack():
    result = calc_profit([60, 100, 120], [10, 20, 30], 50)
    assert result == 240


def test_calc_profit_equal_profit_weight_ratios():
    result = calc_profit([10, 20, 30], [10, 20, 30], 40)
    assert result == 40


def test_calc_profit_zero_weight_items():
    result = calc_profit([10, 20], [0, 5], 10)
    assert result == float('inf')


def test_calc_profit_zero_profit_items():
    result = calc_profit([0, 0, 10], [5, 10, 5], 10)
    assert result == 10


def test_calc_profit_large_capacity():
    result = calc_profit([5, 10, 15], [2, 3, 5], 1000)
    assert result == 30


def test_calc_profit_empty_lists():
    result = calc_profit([], [], 10)
    assert result == 0


def test_calc_profit_mismatched_lengths():
    with pytest.raises(ValueError, match="The length of profit and weight must be same."):
        calc_profit([1, 2, 3], [1, 2], 10)


def test_calc_profit_negative_max_weight():
    with pytest.raises(ValueError, match="max_weight must greater than zero."):
        calc_profit([10, 20], [5, 10], -5)


def test_calc_profit_zero_max_weight():
    with pytest.raises(ValueError, match="max_weight must greater than zero."):
        calc_profit([10, 20], [5, 10], 0)


def test_calc_profit_negative_profit():
    with pytest.raises(ValueError, match="Profit can not be negative."):
        calc_profit([10, -5, 20], [5, 10, 15], 20)


def test_calc_profit_negative_weight():
    with pytest.raises(ValueError, match="Weight can not be negative."):
        calc_profit([10, 20, 30], [5, -10, 15], 20)


def test_calc_profit_multiple_items_same_ratio():
    result = calc_profit([10, 20, 10], [5, 10, 5], 15)
    assert result == 40


def test_calc_profit_high_value_low_weight():
    result = calc_profit([100, 10, 5], [1, 10, 20], 15)
    assert result == 150