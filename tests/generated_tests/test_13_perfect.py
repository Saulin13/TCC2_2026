import sys
import os
sys.path.append(r'C:\Users\diogo\OneDrive\Área de Trabalho\Diogo\PUC\8 Periodo\TCC\TCC2_2026/repos/Python')
from maths.perfect_number import perfect
import os
import sys




import pytest

def test_perfect():
    # Test cases for perfect numbers
    assert perfect(6) == True
    assert perfect(28) == True
    assert perfect(496) == True
    assert perfect(8128) == True
    assert perfect(33550336) == True

    # Test cases for non-perfect numbers
    assert perfect(27) == False
    assert perfect(29) == False
    assert perfect(12) == False
    assert perfect(0) == False
    assert perfect(-1) == False
    assert perfect(33550337) == False
    assert perfect(1) == False

    # Test cases for invalid input
    with pytest.raises(ValueError):
        perfect("123")
    with pytest.raises(ValueError):
        perfect(12.34)
    with pytest.raises(ValueError):
        perfect("Hello")
