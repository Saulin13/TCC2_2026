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


def test_palindromic_string_all_same_characters():
    assert palindromic_string('aaaa') == 'aaaa'


def test_palindromic_string_no_palindrome_longer_than_one():
    result = palindromic_string('abcdef')
    assert len(result) == 1
    assert result in ['a', 'b', 'c', 'd', 'e', 'f']


def test_palindromic_string_palindrome_at_start():
    assert palindromic_string('racecarxyz') == 'racecar'


def test_palindromic_string_palindrome_at_end():
    assert palindromic_string('xyzracecar') == 'racecar'


def test_palindromic_string_palindrome_in_middle():
    assert palindromic_string('xyzabcdcbaqrs') == 'abcdcba'


def test_palindromic_string_entire_string_palindrome():
    assert palindromic_string('racecar') == 'racecar'


def test_palindromic_string_even_length_palindrome():
    assert palindromic_string('abccba') == 'abccba'


def test_palindromic_string_mixed_case_sensitive():
    result = palindromic_string('Aa')
    assert result in ['A', 'a']


def test_palindromic_string_with_spaces():
    assert palindromic_string('a b a') == 'a b a'


def test_palindromic_string_with_numbers():
    assert palindromic_string('12321') == '12321'


def test_palindromic_string_with_special_characters():
    assert palindromic_string('a!b!a') == 'a!b!a'


def test_palindromic_string_longer_string():
    assert palindromic_string('forgeeksskeegfor') == 'geeksskeeg'


def test_palindromic_string_multiple_palindromes_returns_longest():
    result = palindromic_string('abacabad')
    assert result == 'abacaba'


def test_palindromic_string_empty_string_raises_exception():
    with pytest.raises(IndexError):
        palindromic_string('')


def test_palindromic_string_three_characters_palindrome():
    assert palindromic_string('aba') == 'aba'


def test_palindromic_string_four_characters_palindrome():
    assert palindromic_string('abba') == 'abba'