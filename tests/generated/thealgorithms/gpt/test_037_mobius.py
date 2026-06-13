import pytest
from maths.mobius_function import mobius

def test_mobius_normal_cases():
    assert mobius(1) == 1
    assert mobius(2) == -1
    assert mobius(3) == -1
    assert mobius(4) == 0
    assert mobius(5) == -1
    assert mobius(6) == 1
    assert mobius(30) == 1

def test_mobius_edge_cases():
    assert mobius(0) == 0
    assert mobius(-1) == 1
    assert mobius(10**400) == 0
    assert mobius(10**-400) == 1
    assert mobius(-1424) == 1

def test_mobius_invalid_input():
    with pytest.raises(TypeError):
        mobius('asd')
    with pytest.raises(TypeError):
        mobius([1, '2', 2.0])
    with pytest.raises(TypeError):
        mobius(None)