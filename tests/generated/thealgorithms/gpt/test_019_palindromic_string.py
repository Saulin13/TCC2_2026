import pytest
from strings.manacher import palindromic_string

def test_palindromic_string_normal_cases():
    assert palindromic_string('abbbaba') == 'abbba'
    assert palindromic_string('ababa') == 'ababa'
    assert palindromic_string('racecar') == 'racecar'
    assert palindromic_string('banana') == 'anana'
    assert palindromic_string('civic') == 'civic'

def test_palindromic_string_edge_cases():
    assert palindromic_string('') == ''
    assert palindromic_string('a') == 'a'
    assert palindromic_string('aa') == 'aa'
    assert palindromic_string('ab') == 'a'  # or 'b', both are correct
    assert palindromic_string('abc') == 'a'  # or 'b' or 'c', all are correct

def test_palindromic_string_failure_cases():
    with pytest.raises(TypeError):
        palindromic_string(None)