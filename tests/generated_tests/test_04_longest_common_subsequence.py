import sys
import os
sys.path.append(r'C:\Users\diogo\OneDrive\Área de Trabalho\Diogo\PUC\8 Periodo\TCC\TCC2_2026/repos/Python')
from dynamic_programming.longest_common_subsequence import longest_common_subsequence
import os
import sys




import pytest


def test_longest_common_subsequence():
    assert longest_common_subsequence("programming", "gaming") == (6, 'gaming')
    assert longest_common_subsequence("physics", "smartphone") == (2, 'ph')
    assert longest_common_subsequence("computer", "food") == (1, 'o')
    assert longest_common_subsequence("", "abc") == (0, '')
    assert longest_common_subsequence("abc", "") == (0, '')
    assert longest_common_subsequence("", "") == (0, '')
    assert longest_common_subsequence("abc", "def") == (0, '')
    assert longest_common_subsequence("abc", "abc") == (3, 'abc')
    assert longest_common_subsequence("a", "a") == (1, 'a')
    assert longest_common_subsequence("a", "b") == (0, '')
    assert longest_common_subsequence("abcdef", "ace") == (3, 'ace')
    assert longest_common_subsequence("ABCD", "ACBD") == (3, 'ABD')

if __name__ == "__main__":
    pytest.main()
