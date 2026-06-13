import pytest
from strings.manacher import palindromic_string


def test_palindromic_string_basic_odd_length():
    assert palindromic_string('ababa') == 'ababa'


def test_palindromic_string_basic_even_length():
    assert palindromic_string('abbbaba') == 'abbba'


def test_palindromic_string_single_character():
    assert palindromic_string('a') == 'a'


def test_palindromic_string_two_characters_same():
    assert palindromic_string('aa') == 'aa'


def test_palindromic_string_two_characters_different():
    result = palindromic_string('ab')
    assert result in ['a', 'b']


def test_palindromic_string_entire_string_palindrome():
    assert palindromic_string('racecar') == 'racecar'


def test_palindromic_string_no_palindrome_longer_than_one():
    result = palindromic_string('abcdef')
    assert len(result) == 1
    assert result in ['a', 'b', 'c', 'd', 'e', 'f']


def test_palindromic_string_palindrome_at_start():
    assert palindromic_string('aabcde') == 'aa'


def test_palindromic_string_palindrome_at_end():
    assert palindromic_string('abcdee') == 'ee'


def test_palindromic_string_palindrome_in_middle():
    assert palindromic_string('abcddcba') == 'abcddcba'


def test_palindromic_string_multiple_palindromes():
    result = palindromic_string('aabbccbb')
    assert result in ['bb', 'aa', 'cc', 'bbccbb']


def test_palindromic_string_long_palindrome():
    assert palindromic_string('xabcdcbay') == 'abcdcba'


def test_palindromic_string_all_same_characters():
    assert palindromic_string('aaaaa') == 'aaaaa'


def test_palindromic_string_even_length_palindrome():
    assert palindromic_string('abccba') == 'abccba'


def test_palindromic_string_odd_length_palindrome():
    assert palindromic_string('abcba') == 'abcba'


def test_palindromic_string_complex_case():
    assert palindromic_string('forgeeksskeegfor') == 'geeksskeeg'


def test_palindromic_string_with_spaces():
    result = palindromic_string('a b a')
    assert result == 'a b a'


def test_palindromic_string_with_numbers():
    assert palindromic_string('12321') == '12321'


def test_palindromic_string_mixed_characters():
    assert palindromic_string('abc1221xyz') == '1221'


def test_palindromic_string_empty_string():
    with pytest.raises(IndexError):
        palindromic_string('')