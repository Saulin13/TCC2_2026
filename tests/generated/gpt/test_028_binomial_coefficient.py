import pytest
from data_structures.binary_tree.number_of_possible_binary_trees import binomial_coefficient

def test_binomial_coefficient_normal_cases():
    assert binomial_coefficient(4, 2) == 6
    assert binomial_coefficient(5, 2) == 10
    assert binomial_coefficient(6, 3) == 20
    assert binomial_coefficient(10, 5) == 252

def test_binomial_coefficient_edge_cases():
    assert binomial_coefficient(0, 0) == 1
    assert binomial_coefficient(1, 0) == 1
    assert binomial_coefficient(1, 1) == 1
    assert binomial_coefficient(5, 0) == 1
    assert binomial_coefficient(5, 5) == 1

def test_binomial_coefficient_k_greater_than_n():
    assert binomial_coefficient(4, 5) == 0
    assert binomial_coefficient(3, 4) == 0

def test_binomial_coefficient_negative_values():
    with pytest.raises(ValueError):
        binomial_coefficient(-1, 2)
    with pytest.raises(ValueError):
        binomial_coefficient(4, -2)
    with pytest.raises(ValueError):
        binomial_coefficient(-4, -2)

def test_binomial_coefficient_large_values():
    assert binomial_coefficient(20, 10) == 184756
    assert binomial_coefficient(30, 15) == 155117520