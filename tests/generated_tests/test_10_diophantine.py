import sys
import os
sys.path.append(r'C:\Users\diogo\OneDrive\Área de Trabalho\Diogo\PUC\8 Periodo\TCC\TCC2_2026/repos/Python')
from blockchain.diophantine_equation import diophantine
import os
import sys




import pytest

def test_diophantine():
    # Test case 1
    result = diophantine(10, 6, 14)
    assert result == (-7.0, 14.0), f"Expected (-7.0, 14.0), got {result}"

    # Test case 2
    result = diophantine(391, 299, -69)
    assert result == (9.0, -12.0), f"Expected (9.0, -12.0), got {result}"

    # Test case 3: Edge case where a or b is zero
    result = diophantine(0, 5, 10)
    assert result == (0.0, 2.0), f"Expected (0.0, 2.0), got {result}"

    # Test case 4: Edge case where c is zero
    result = diophantine(7, 5, 0)
    assert result == (0.0, 0.0), f"Expected (0.0, 0.0), got {result}"

    # Test case 5: Edge case where a, b, and c are zero
    with pytest.raises(AssertionError):
        diophantine(0, 0, 0)

# Note: The functions `greatest_common_divisor` and `extended_gcd` need to be defined
# for this test to run successfully.
