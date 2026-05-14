import sys
import os
sys.path.append(r'C:\Users\diogo\OneDrive\Área de Trabalho\Diogo\PUC\8 Periodo\TCC\TCC2_2026/repos/Python')
from project_euler.problem_086.sol1 import solution
import os
import sys




import pytest
from math import sqrt

def test_solution():
    assert solution(100) == 24
    assert solution(1000) == 72
    assert solution(2000) == 100
    assert solution(20000) == 288
    # Additional test cases
    assert solution(500) == 48
    assert solution(1500) == 86
    assert solution(5000) == 154
    assert solution(10000) == 206
