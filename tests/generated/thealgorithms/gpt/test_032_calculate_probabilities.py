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
    assert calculate_probabilities(1_000_000, 10_000_000) == 0.1

def test_calculate_probabilities_failure_negative_instances():
    with pytest.raises(ValueError):
        calculate_probabilities(-10, 100)

def test_calculate_probabilities_failure_negative_total():
    with pytest.raises(ValueError):
        calculate_probabilities(10, -100)
```

Note: The function `calculate_probabilities` as provided does not currently handle negative values or raise exceptions for them. If you want to handle such cases, you would need to modify the function to include checks for negative values and raise appropriate exceptions.