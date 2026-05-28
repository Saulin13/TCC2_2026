import pytest
from maths.sock_merchant import sock_merchant

def test_sock_merchant_normal_case():
    assert sock_merchant([10, 20, 20, 10, 10, 30, 50, 10, 20]) == 3
    assert sock_merchant([1, 1, 3, 3]) == 2
    assert sock_merchant([5, 5, 5, 5, 5, 5]) == 3

def test_sock_merchant_no_pairs():
    assert sock_merchant([1, 2, 3, 4, 5]) == 0
    assert sock_merchant([]) == 0

def test_sock_merchant_all_pairs():
    assert sock_merchant([2, 2, 2, 2, 2, 2, 2, 2]) == 4
    assert sock_merchant([7, 7, 7, 7]) == 2

def test_sock_merchant_single_color():
    assert sock_merchant([9, 9, 9, 9, 9]) == 2
    assert sock_merchant([8]) == 0

def test_sock_merchant_large_input():
    assert sock_merchant([1] * 1000) == 500
    assert sock_merchant([1, 2] * 500) == 500

def test_sock_merchant_invalid_input():
    with pytest.raises(TypeError):
        sock_merchant(None)
    with pytest.raises(TypeError):
        sock_merchant("not a list")