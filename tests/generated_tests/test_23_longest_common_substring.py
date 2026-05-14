import sys
import os
sys.path.append(r'C:\Users\diogo\OneDrive\Área de Trabalho\Diogo\PUC\8 Periodo\TCC\TCC2_2026/repos/Python')
from dynamic_programming.longest_common_substring import longest_common_substring
import os
import sys




import pytest

def test_longest_common_substring():
    assert longest_common_substring("", "") == ""
    assert longest_common_substring("a", "") == ""
    assert longest_common_substring("", "a") == ""
    assert longest_common_substring("a", "a") == "a"
    assert longest_common_substring("abcdef", "bcd") == "bcd"
    assert longest_common_substring("abcdef", "xabded") == "ab"
    assert longest_common_substring("GeeksforGeeks", "GeeksQuiz") == "Geeks"
    assert longest_common_substring("abcdxyz", "xyzabcd") == "abcd"
    assert longest_common_substring("zxabcdezy", "yzabcdezx") == "abcdez"
    assert longest_common_substring("OldSite:GeeksforGeeks.org", "NewSite:GeeksQuiz.com") == "Site:Geeks"

    with pytest.raises(ValueError):
        longest_common_substring(1, 1)
