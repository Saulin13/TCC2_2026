import pytest
from bit_manipulation.highest_set_bit import get_highest_set_bit_position


def test_get_highest_set_bit_position_normal_case_25():
    assert get_highest_set_bit_position(25) == 5


def test_get_highest_set_bit_position_normal_case_37():
    assert get_highest_set_bit_position(37) == 6


def test_get_highest_set_bit_position_single_bit_set():
    assert get_highest_set_bit_position(1) == 1


def test_get_highest_set_bit_position_power_of_two():
    assert get_highest_set_bit_position(4) == 3


def test_get_highest_set_bit_position_zero():
    assert get_highest_set_bit_position(0) == 0


def test_get_highest_set_bit_position_large_number():
    assert get_highest_set_bit_position(255) == 8


def test_get_highest_set_bit_position_power_of_two_large():
    assert get_highest_set_bit_position(128) == 8


def test_get_highest_set_bit_position_power_of_two_16():
    assert get_highest_set_bit_position(16) == 5


def test_get_highest_set_bit_position_two():
    assert get_highest_set_bit_position(2) == 2


def test_get_highest_set_bit_position_max_byte():
    assert get_highest_set_bit_position(256) == 9


def test_get_highest_set_bit_position_large_value():
    assert get_highest_set_bit_position(1024) == 11


def test_get_highest_set_bit_position_odd_number():
    assert get_highest_set_bit_position(63) == 6


def test_get_highest_set_bit_position_float_raises_type_error():
    with pytest.raises(TypeError, match="Input value must be an 'int' type"):
        get_highest_set_bit_position(0.8)


def test_get_highest_set_bit_position_string_raises_type_error():
    with pytest.raises(TypeError, match="Input value must be an 'int' type"):
        get_highest_set_bit_position("25")


def test_get_highest_set_bit_position_none_raises_type_error():
    with pytest.raises(TypeError, match="Input value must be an 'int' type"):
        get_highest_set_bit_position(None)


def test_get_highest_set_bit_position_list_raises_type_error():
    with pytest.raises(TypeError, match="Input value must be an 'int' type"):
        get_highest_set_bit_position([25])


def test_get_highest_set_bit_position_negative_number():
    assert get_highest_set_bit_position(-1) == 0