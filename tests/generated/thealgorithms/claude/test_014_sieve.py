import pytest
import math
from maths.segmented_sieve import sieve


def test_sieve_small_number():
    assert sieve(8) == [2, 3, 5, 7]


def test_sieve_medium_number():
    assert sieve(27) == [2, 3, 5, 7, 11, 13, 17, 19, 23]


def test_sieve_single_prime():
    assert sieve(2) == [2]


def test_sieve_three():
    assert sieve(3) == [2, 3]


def test_sieve_ten():
    assert sieve(10) == [2, 3, 5, 7]


def test_sieve_twenty():
    assert sieve(20) == [2, 3, 5, 7, 11, 13, 17, 19]


def test_sieve_fifty():
    expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    assert sieve(50) == expected


def test_sieve_one_hundred():
    expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    assert sieve(100) == expected


def test_sieve_one():
    assert sieve(1) == []


def test_sieve_zero_raises_value_error():
    with pytest.raises(ValueError, match="Number 0 must instead be a positive integer"):
        sieve(0)


def test_sieve_negative_raises_value_error():
    with pytest.raises(ValueError, match="Number -1 must instead be a positive integer"):
        sieve(-1)


def test_sieve_negative_large_raises_value_error():
    with pytest.raises(ValueError, match="Number -100 must instead be a positive integer"):
        sieve(-100)


def test_sieve_float_raises_value_error():
    with pytest.raises(ValueError, match="Number 22.2 must instead be a positive integer"):
        sieve(22.2)


def test_sieve_float_positive_raises_value_error():
    with pytest.raises(ValueError, match="Number 5.5 must instead be a positive integer"):
        sieve(5.5)


def test_sieve_float_negative_raises_value_error():
    with pytest.raises(ValueError, match="Number -3.14 must instead be a positive integer"):
        sieve(-3.14)


def test_sieve_large_number():
    result = sieve(200)
    assert 2 in result
    assert 199 in result
    assert 197 in result
    assert len(result) == 46
    assert all(isinstance(p, int) for p in result)