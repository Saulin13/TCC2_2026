import pytest
from collections import Counter
from maths.sock_merchant import sock_merchant


def test_sock_merchant_basic_case():
    assert sock_merchant([10, 20, 20, 10, 10, 30, 50, 10, 20]) == 3


def test_sock_merchant_all_pairs():
    assert sock_merchant([1, 1, 3, 3]) == 2


def test_sock_merchant_no_pairs():
    assert sock_merchant([1, 2, 3, 4, 5]) == 0


def test_sock_merchant_all_same_color_even():
    assert sock_merchant([5, 5, 5, 5, 5, 5]) == 3


def test_sock_merchant_all_same_color_odd():
    assert sock_merchant([7, 7, 7, 7, 7]) == 2


def test_sock_merchant_empty_list():
    assert sock_merchant([]) == 0


def test_sock_merchant_single_sock():
    assert sock_merchant([42]) == 0


def test_sock_merchant_two_matching_socks():
    assert sock_merchant([8, 8]) == 1


def test_sock_merchant_three_matching_socks():
    assert sock_merchant([9, 9, 9]) == 1


def test_sock_merchant_multiple_colors_mixed():
    assert sock_merchant([1, 2, 1, 2, 1, 3, 2]) == 2


def test_sock_merchant_large_numbers():
    assert sock_merchant([100, 200, 100, 300, 200, 100]) == 2


def test_sock_merchant_many_socks_same_color():
    assert sock_merchant([1] * 10) == 5


def test_sock_merchant_many_socks_different_colors():
    assert sock_merchant([1, 2, 3, 1, 2, 3, 1, 2, 3, 1]) == 4


def test_sock_merchant_negative_numbers():
    assert sock_merchant([-1, -1, -2, -2, -3]) == 2


def test_sock_merchant_zero_values():
    assert sock_merchant([0, 0, 0, 0]) == 2


def test_sock_merchant_mixed_positive_negative():
    assert sock_merchant([-5, 5, -5, 5, 10, 10]) == 3


def test_sock_merchant_invalid_input_type():
    with pytest.raises((TypeError, AttributeError)):
        sock_merchant(None)


def test_sock_merchant_invalid_input_string():
    with pytest.raises((TypeError, AttributeError)):
        sock_merchant("not a list")


def test_sock_merchant_invalid_input_number():
    with pytest.raises((TypeError, AttributeError)):
        sock_merchant(123)
```