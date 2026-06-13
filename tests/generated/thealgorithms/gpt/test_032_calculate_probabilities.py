import pytest
from machine_learning.linear_discriminant_analysis import calculate_probabilities

def test_calculate_probabilities_normal_case():
    assert calculate_probabilities(20, 60) == 0.3333333333333333
    assert calculate_probabilities(30, 100) == 0.3
    assert calculate_probabilities(50, 200) == 0.25

def test_calculate_probabilities_edge_case_zero_instances():
    assert calculate_probabilities(0, 100) == 0.0

def test_calculate_probabilities_edge_case_equal_instances_and_total():
    assert calculate_probabilities(100, 100) == 1.0

def test_calculate_probabilities_edge_case_zero_total():
    with pytest.raises(ZeroDivisionError):
        calculate_probabilities(10, 0)

def test_calculate_probabilities_edge_case_large_numbers():
    assert calculate_probabilities(1000000, 1000000) == 1.0
    assert calculate_probabilities(500000, 1000000) == 0.5

def test_calculate_probabilities_failure_negative_instances():
    with pytest.raises(ValueError):
        calculate_probabilities(-10, 100)

def test_calculate_probabilities_failure_negative_total():
    with pytest.raises(ValueError):
        calculate_probabilities(10, -100)
```

Note: The original function does not handle negative values or zero division explicitly, so the tests for negative values will fail unless the function is modified to raise `ValueError` for negative inputs.