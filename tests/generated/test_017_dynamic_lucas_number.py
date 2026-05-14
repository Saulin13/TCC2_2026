import pytest
from maths.lucas_series import dynamic_lucas_number

def test_dynamic_lucas_number_normal_cases():
    assert dynamic_lucas_number(0) == 2
    assert dynamic_lucas_number(1) == 1
    assert dynamic_lucas_number(2) == 3
    assert dynamic_lucas_number(3) == 4
    assert dynamic_lucas_number(4) == 7
    assert dynamic_lucas_number(5) == 11
    assert dynamic_lucas_number(10) == 123
    assert dynamic_lucas_number(20) == 15127
    assert dynamic_lucas_number(25) == 167761

def test_dynamic_lucas_number_edge_cases():
    assert dynamic_lucas_number(0) == 2
    assert dynamic_lucas_number(1) == 1

def test_dynamic_lucas_number_invalid_input():
    with pytest.raises(TypeError, match="dynamic_lucas_number accepts only integer arguments."):
        dynamic_lucas_number(-1.5)
    with pytest.raises(TypeError, match="dynamic_lucas_number accepts only integer arguments."):
        dynamic_lucas_number("string")
    with pytest.raises(TypeError, match="dynamic_lucas_number accepts only integer arguments."):
        dynamic_lucas_number(None)