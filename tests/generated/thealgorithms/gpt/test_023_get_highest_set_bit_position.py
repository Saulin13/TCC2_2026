import pytest
from bit_manipulation.highest_set_bit import get_highest_set_bit_position

def test_highest_set_bit_normal_cases():
    assert get_highest_set_bit_position(25) == 5
    assert get_highest_set_bit_position(37) == 6
    assert get_highest_set_bit_position(1) == 1
    assert get_highest_set_bit_position(4) == 3

def test_highest_set_bit_edge_cases():
    assert get_highest_set_bit_position(0) == 0
    assert get_highest_set_bit_position(2**31 - 1) == 31  # Maximum 32-bit signed integer
    assert get_highest_set_bit_position(2**63 - 1) == 63  # Maximum 64-bit signed integer

def test_highest_set_bit_invalid_input():
    with pytest.raises(TypeError, match="Input value must be an 'int' type"):
        get_highest_set_bit_position(0.8)
    with pytest.raises(TypeError, match="Input value must be an 'int' type"):
        get_highest_set_bit_position("string")
    with pytest.raises(TypeError, match="Input value must be an 'int' type"):
        get_highest_set_bit_position(None)