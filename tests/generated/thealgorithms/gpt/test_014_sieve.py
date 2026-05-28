import pytest
from maths.segmented_sieve import sieve

def test_sieve_normal_cases():
    assert sieve(8) == [2, 3, 5, 7]
    assert sieve(27) == [2, 3, 5, 7, 11, 13, 17, 19, 23]
    assert sieve(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

def test_sieve_edge_cases():
    assert sieve(2) == [2]
    assert sieve(3) == [2, 3]

def test_sieve_invalid_input():
    with pytest.raises(ValueError, match="Number 0 must instead be a positive integer"):
        sieve(0)
    with pytest.raises(ValueError, match="Number -1 must instead be a positive integer"):
        sieve(-1)
    with pytest.raises(ValueError, match="Number 22.2 must instead be a positive integer"):
        sieve(22.2)