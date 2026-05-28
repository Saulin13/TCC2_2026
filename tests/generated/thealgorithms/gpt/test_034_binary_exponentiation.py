import pytest
from maths.fermat_little_theorem import binary_exponentiation

def test_binary_exponentiation_normal_cases():
    assert binary_exponentiation(2, 10, 1000) == 24
    assert binary_exponentiation(3, 5, 13) == 5
    assert binary_exponentiation(5, 3, 7) == 6
    assert binary_exponentiation(10, 3, 100) == 0

def test_binary_exponentiation_edge_cases():
    assert binary_exponentiation(2, 0, 1000) == 1
    assert binary_exponentiation(0, 0, 1) == 1
    assert binary_exponentiation(1, 1000, 1000) == 1
    assert binary_exponentiation(0, 5, 1000) == 0

def test_binary_exponentiation_large_exponent():
    assert binary_exponentiation(2, 100, 1000) == 376

def test_binary_exponentiation_failure_cases():
    with pytest.raises(RecursionError):
        binary_exponentiation(2, -1, 1000)