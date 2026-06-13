import pytest
from maths.mobius_function import mobius


def test_mobius_square_free_even_factors():
    assert mobius(6) == 1
    assert mobius(10) == 1
    assert mobius(15) == 1
    assert mobius(30) == -1


def test_mobius_square_free_odd_factors():
    assert mobius(2) == -1
    assert mobius(3) == -1
    assert mobius(5) == -1
    assert mobius(7) == -1
    assert mobius(11) == -1


def test_mobius_not_square_free():
    assert mobius(4) == 0
    assert mobius(8) == 0
    assert mobius(9) == 0
    assert mobius(12) == 0
    assert mobius(18) == 0
    assert mobius(24) == 0
    assert mobius(27) == 0


def test_mobius_one():
    assert mobius(1) == 1


def test_mobius_negative_numbers():
    assert mobius(-1) == 1
    assert mobius(-2) == -1
    assert mobius(-3) == -1
    assert mobius(-6) == 1
    assert mobius(-1424) == 1


def test_mobius_large_numbers():
    assert mobius(10**400) == 0
    assert mobius(10**-400) == 1


def test_mobius_composite_square_free():
    assert mobius(105) == -1
    assert mobius(210) == 1


def test_mobius_invalid_type_string():
    with pytest.raises(TypeError):
        mobius('asd')


def test_mobius_invalid_type_list():
    with pytest.raises(TypeError):
        mobius([1, '2', 2.0])


def test_mobius_invalid_type_dict():
    with pytest.raises(TypeError):
        mobius({'key': 'value'})


def test_mobius_invalid_type_none():
    with pytest.raises(TypeError):
        mobius(None)