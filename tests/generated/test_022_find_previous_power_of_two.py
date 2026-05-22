import pytest
from bit_manipulation.find_previous_power_of_two import find_previous_power_of_two

def test_find_previous_power_of_two_normal_cases():
    assert find_previous_power_of_two(0) == 0
    assert find_previous_power_of_two(1) == 1
    assert find_previous_power_of_two(2) == 2
    assert find_previous_power_of_two(3) == 2
    assert find_previous_power_of_two(4) == 4
    assert find_previous_power_of_two(5) == 4
    assert find_previous_power_of_two(6) == 4
    assert find_previous_power_of_two(7) == 4
    assert find_previous_power_of_two(8) == 8
    assert find_previous_power_of_two(9) == 8
    assert find_previous_power_of_two(16) == 16
    assert find_previous_power_of_two(17) == 16

def test_find_previous_power_of_two_edge_cases():
    assert find_previous_power_of_two(1024) == 1024
    assert find_previous_power_of_two(1025) == 1024
    assert find_previous_power_of_two(2048) == 2048

def test_find_previous_power_of_two_invalid_input():
    with pytest.raises(ValueError, match="Input must be a non-negative integer"):
        find_previous_power_of_two(-1)
    with pytest.raises(ValueError, match="Input must be a non-negative integer"):
        find_previous_power_of_two(-100)
    with pytest.raises(ValueError, match="Input must be a non-negative integer"):
        find_previous_power_of_two(10.5)
    with pytest.raises(ValueError, match="Input must be a non-negative integer"):
        find_previous_power_of_two("string")