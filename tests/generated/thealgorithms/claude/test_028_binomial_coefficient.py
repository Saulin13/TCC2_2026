import pytest
from data_structures.binary_tree.number_of_possible_binary_trees import binomial_coefficient


def test_binomial_coefficient_basic():
    assert binomial_coefficient(4, 2) == 6


def test_binomial_coefficient_choose_zero():
    assert binomial_coefficient(5, 0) == 1


def test_binomial_coefficient_choose_all():
    assert binomial_coefficient(5, 5) == 1


def test_binomial_coefficient_choose_one():
    assert binomial_coefficient(10, 1) == 10


def test_binomial_coefficient_symmetric():
    assert binomial_coefficient(10, 3) == binomial_coefficient(10, 7)


def test_binomial_coefficient_larger_values():
    assert binomial_coefficient(10, 5) == 252


def test_binomial_coefficient_small_n_large_k():
    assert binomial_coefficient(5, 3) == 10


def test_binomial_coefficient_edge_case_zero_zero():
    assert binomial_coefficient(0, 0) == 1


def test_binomial_coefficient_large_n_small_k():
    assert binomial_coefficient(100, 2) == 4950


def test_binomial_coefficient_large_n_large_k():
    assert binomial_coefficient(20, 10) == 184756


def test_binomial_coefficient_n_choose_n_minus_one():
    assert binomial_coefficient(7, 6) == 7


def test_binomial_coefficient_pascal_triangle():
    assert binomial_coefficient(6, 2) == 15
    assert binomial_coefficient(6, 3) == 20
    assert binomial_coefficient(6, 4) == 15


def test_binomial_coefficient_negative_k():
    result = binomial_coefficient(5, -1)
    assert result == 1


def test_binomial_coefficient_k_greater_than_n():
    result = binomial_coefficient(3, 5)
    assert result == 1