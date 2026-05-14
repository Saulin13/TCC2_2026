import sys
import os
sys.path.append(r'C:\Users\diogo\OneDrive\Área de Trabalho\Diogo\PUC\8 Periodo\TCC\TCC2_2026/repos/Python')
from ciphers.mixed_keyword_cypher import mixed_keyword
import os
import sys




import pytest

def test_mixed_keyword():
    # Test case 1: Verbose mode
    result = mixed_keyword("college", "UNIVERSITY", True)
    expected_mapping = {
        'A': 'C', 'B': 'A', 'C': 'I', 'D': 'P', 'E': 'U', 'F': 'Z', 'G': 'O', 'H': 'B',
        'I': 'J', 'J': 'Q', 'K': 'V', 'L': 'L', 'M': 'D', 'N': 'K', 'O': 'R', 'P': 'W',
        'Q': 'E', 'R': 'F', 'S': 'M', 'T': 'S', 'U': 'X', 'V': 'G', 'W': 'H', 'X': 'N',
        'Y': 'T', 'Z': 'Y'
    }
    expected_ciphertext = 'XKJGUFMJST'
    assert result == expected_ciphertext

    # Test case 2: Non-verbose mode
    result = mixed_keyword("college", "UNIVERSITY", False)
    assert result == expected_ciphertext

    # Test case 3: Different keyword and plaintext
    result = mixed_keyword("hello", "WORLD", False)
    expected_ciphertext = 'ZKQPD'
    assert result == expected_ciphertext

    # Test case 4: Keyword with all unique characters
    result = mixed_keyword("abcdef", "HELLO", False)
    expected_ciphertext = 'HFLLO'
    assert result == expected_ciphertext

    # Test case 5: Empty plaintext
    result = mixed_keyword("keyword", "", False)
    expected_ciphertext = ''
    assert result == expected_ciphertext

    # Test case 6: Keyword with non-alphabet characters
    result = mixed_keyword("key123", "TEST", False)
    expected_ciphertext = 'TQST'
    assert result == expected_ciphertext

    # Test case 7: Plaintext with non-alphabet characters
    result = mixed_keyword("keyword", "TEST123", False)
    expected_ciphertext = 'TQST123'
    assert result == expected_ciphertext
