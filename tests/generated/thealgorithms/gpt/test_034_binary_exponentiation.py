import pytest
from maths.fermat_little_theorem import binary_exponentiation

def test_binary_exponentiation_normal_cases():
    assert binary_exponentiation(2, 3, 5) == 3
    assert binary_exponentiation(3, 4, 7) == 4
    assert binary_exponentiation(5, 5, 13) == 8
    assert binary_exponentiation(10, 10, 17) == 15

def test_binary_exponentiation_edge_cases():
    assert binary_exponentiation(2, 0, 5) == 1
    assert binary_exponentiation(0, 0, 5) == 1
    assert binary_exponentiation(0, 5, 5) == 0
    assert binary_exponentiation(1, 1000, 1) == 0
    assert binary_exponentiation(1, 1000, 2) == 1

def test_binary_exponentiation_large_exponent():
    assert binary_exponentiation(2, 100, 1000) == 376
    assert binary_exponentiation(3, 200, 1000) == 1

def test_binary_exponentiation_failure_cases():
    with pytest.raises(TypeError):
        binary_exponentiation(2, '3', 5)
    with pytest.raises(TypeError):
        binary_exponentiation(2, 3, '5')
    with pytest.raises(TypeError):
        binary_exponentiation('2', 3, 5)