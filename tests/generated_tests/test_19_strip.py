import sys
import os
sys.path.append(r'C:\Users\diogo\OneDrive\Área de Trabalho\Diogo\PUC\8 Periodo\TCC\TCC2_2026/repos/Python')
from strings.strip import strip
import os
import sys




import pytest

def test_strip_default_whitespace():
    assert strip("   hello   ") == "hello"
    assert strip("\thello\t") == "hello"
    assert strip("\nhello\n") == "hello"
    assert strip("\rhello\r") == "hello"
    assert strip("hello") == "hello"
    assert strip("") == ""

def test_strip_custom_characters():
    assert strip("...world...", ".") == "world"
    assert strip("123hello123", "123") == "hello"
    assert strip("!!!wow!!!", "!") == "wow"
    assert strip("abcXYZabc", "abc") == "XYZ"
    assert strip("xxxyyyzzz", "xyz") == ""

def test_strip_no_characters_to_strip():
    assert strip("hello", "") == "hello"
    assert strip("world", "") == "world"

def test_strip_edge_cases():
    assert strip("   ", " ") == ""
    assert strip("...", ".") == ""
    assert strip("123", "123") == ""
    assert strip("a", "a") == ""
    assert strip("a", "b") == "a"

if __name__ == "__main__":
    pytest.main()
