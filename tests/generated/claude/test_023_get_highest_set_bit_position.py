import pytest
from bit_manipulation.highest_set_bit import get_highest_set_bit_position


def test_get_highest_set_bit_position_normal_cases():
    assert get_highest_set_bit_position(25) == 5
    assert get_highest_set_bit_position(37) == 6
    assert get_highest_set_bit_position(1) == 1
    assert get_highest_set_bit_position(4) == 3


def test_get_highest_set_bit_position_edge_case_zero():
    assert get_highest_set_bit_position(0) == 0


def test_get_highest_set_bit_position_edge_case_powers_of_two():
    assert get_highest_set_bit_position(2) == 2
    assert get_highest_set_bit_position(8) == 4
    assert get_highest_set_bit_position(16) == 5
    assert get_highest_set_bit_position(32) == 6
    assert get_highest_set_bit_position(64) == 7
    assert get_highest_set_bit_position(128) == 8
    assert get_highest_set_bit_position(256) == 9
    assert get_highest_set_bit_position(1024) == 11


def test_get_highest_set_bit_position_large_numbers():
    assert get_highest_set_bit_position(255) == 8
    assert get_highest_set_bit_position(1000) == 10
    assert get_highest_set_bit_position(65535) == 16
    assert get_highest_set_bit_position(1048576) == 21


def test_get_highest_set_bit_position_small_numbers():
    assert get_highest_set_bit_position(3) == 2
    assert get_highest_set_bit_position(5) == 3
    assert get_highest_set_bit_position(7) == 3
    assert get_highest_set_bit_position(15) == 4


def test_get_highest_set_bit_position_type_error_float():
    with pytest.raises(TypeError, match="Input value must be an 'int' type"):
        get_highest_set_bit_position(0.8)


def test_get_highest_set_bit_position_type_error_string():
    with pytest.raises(TypeError, match="Input value must be an 'int' type"):
        get_highest_set_bit_position("25")


def test_get_highest_set_bit_position_type_error_none():
    with pytest.raises(TypeError, match="Input value must be an 'int' type"):
        get_highest_set_bit_position(None)


def test_get_highest_set_bit_position_type_error_list():
    with pytest.raises(TypeError, match="Input value must be an 'int' type"):
        get_highest_set_bit_position([25])


def test_get_highest_set_bit_position_negative_numbers():
    assert get_highest_set_bit_position(-1) == 0
    assert get_highest_set_bit_position(-5) == 0
    assert get_highest_set_bit_position(-100) == 0