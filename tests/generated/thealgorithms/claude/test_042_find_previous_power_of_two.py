import pytest
from bit_manipulation.find_previous_power_of_two import find_previous_power_of_two


def test_zero():
    assert find_previous_power_of_two(0) == 0


def test_one():
    assert find_previous_power_of_two(1) == 1


def test_exact_powers_of_two():
    assert find_previous_power_of_two(2) == 2
    assert find_previous_power_of_two(4) == 4
    assert find_previous_power_of_two(8) == 8
    assert find_previous_power_of_two(16) == 16
    assert find_previous_power_of_two(32) == 32
    assert find_previous_power_of_two(64) == 64
    assert find_previous_power_of_two(128) == 128
    assert find_previous_power_of_two(256) == 256
    assert find_previous_power_of_two(1024) == 1024


def test_non_powers_of_two():
    assert find_previous_power_of_two(3) == 2
    assert find_previous_power_of_two(5) == 4
    assert find_previous_power_of_two(6) == 4
    assert find_previous_power_of_two(7) == 4
    assert find_previous_power_of_two(9) == 8
    assert find_previous_power_of_two(10) == 8
    assert find_previous_power_of_two(15) == 8
    assert find_previous_power_of_two(17) == 16
    assert find_previous_power_of_two(31) == 16
    assert find_previous_power_of_two(33) == 32
    assert find_previous_power_of_two(100) == 64
    assert find_previous_power_of_two(255) == 128
    assert find_previous_power_of_two(1000) == 512


def test_large_numbers():
    assert find_previous_power_of_two(1000000) == 524288
    assert find_previous_power_of_two(1048576) == 1048576
    assert find_previous_power_of_two(1048577) == 1048576


def test_range_sequence():
    result = [find_previous_power_of_two(i) for i in range(18)]
    expected = [0, 1, 2, 2, 4, 4, 4, 4, 8, 8, 8, 8, 8, 8, 8, 8, 16, 16]
    assert result == expected


def test_negative_number_raises_error():
    with pytest.raises(ValueError, match="Input must be a non-negative integer"):
        find_previous_power_of_two(-1)
    
    with pytest.raises(ValueError, match="Input must be a non-negative integer"):
        find_previous_power_of_two(-5)
    
    with pytest.raises(ValueError, match="Input must be a non-negative integer"):
        find_previous_power_of_two(-100)


def test_float_raises_error():
    with pytest.raises(ValueError, match="Input must be a non-negative integer"):
        find_previous_power_of_two(10.5)
    
    with pytest.raises(ValueError, match="Input must be a non-negative integer"):
        find_previous_power_of_two(3.14)
    
    with pytest.raises(ValueError, match="Input must be a non-negative integer"):
        find_previous_power_of_two(0.5)


def test_non_integer_types_raise_error():
    with pytest.raises(ValueError, match="Input must be a non-negative integer"):
        find_previous_power_of_two("10")
    
    with pytest.raises(ValueError, match="Input must be a non-negative integer"):
        find_previous_power_of_two(None)
    
    with pytest.raises(ValueError, match="Input must be a non-negative integer"):
        find_previous_power_of_two([10])