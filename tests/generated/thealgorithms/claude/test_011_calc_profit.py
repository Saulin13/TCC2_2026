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


def test_calc_profit_no_items():
    result = calc_profit([], [], 10)
    assert result == 0


def test_calc_profit_zero_max_weight_raises():
    with pytest.raises(ValueError, match="max_weight must greater than zero"):
        calc_profit([1, 2, 3], [3, 4, 5], 0)


def test_calc_profit_negative_max_weight_raises():
    with pytest.raises(ValueError, match="max_weight must greater than zero"):
        calc_profit([1, 2, 3], [3, 4, 5], -5)


def test_calc_profit_mismatched_lengths_raises():
    with pytest.raises(ValueError, match="The length of profit and weight must be same"):
        calc_profit([1, 2, 3], [3, 4], 15)


def test_calc_profit_negative_profit_raises():
    with pytest.raises(ValueError, match="Profit can not be negative"):
        calc_profit([1, -2, 3], [3, 4, 5], 15)


def test_calc_profit_negative_weight_raises():
    with pytest.raises(ValueError, match="Weight can not be negative"):
        calc_profit([1, 2, 3], [3, -4, 5], 15)


def test_calc_profit_all_items_fit():
    result = calc_profit([60, 100, 120], [10, 20, 30], 50)
    assert result == 240


def test_calc_profit_fractional_knapsack():
    result = calc_profit([60, 100, 120], [10, 20, 30], 50)
    assert result == 240


def test_calc_profit_max_weight_less_than_smallest_item():
    result = calc_profit([10, 20, 30], [5, 10, 15], 3)
    assert result == 6


def test_calc_profit_duplicate_profit_weight_ratios():
    result = calc_profit([10, 20], [5, 10], 15)
    assert result == 30


def test_calc_profit_large_max_weight():
    result = calc_profit([10, 20, 30], [5, 10, 15], 1000)
    assert result == 60


def test_calc_profit_zero_profit():
    result = calc_profit([0, 0, 0], [1, 2, 3], 10)
    assert result == 0


def test_calc_profit_mixed_ratios():
    result = calc_profit([100, 60, 120], [20, 10, 30], 50)
    assert result == 240


def test_calc_profit_exact_weight_match():
    result = calc_profit([10, 20, 30], [5, 10, 15], 30)
    assert result == 60