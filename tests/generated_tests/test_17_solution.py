import sys
import os
sys.path.append(r'C:\Users\diogo\OneDrive\Área de Trabalho\Diogo\PUC\8 Periodo\TCC\TCC2_2026/repos/Python')
from project_euler.problem_100.sol1 import solution
import os
import sys




import pytest

def test_solution():
    assert solution(2) == 3
    assert solution(4) == 15
    assert solution(21) == 85
    assert solution(10**12) == 756872327473  # Valor esperado para um min_total de 10**12

if __name__ == "__main__":
    pytest.main()
