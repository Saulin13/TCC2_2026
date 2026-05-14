import sys
import os
sys.path.append(r'C:\Users\diogo\OneDrive\Área de Trabalho\Diogo\PUC\8 Periodo\TCC\TCC2_2026/repos/Python')
from searches.hill_climbing import score
import os
import sys




import pytest

class SearchProblem:
    def __init__(self, x, y, some_other_param, function):
        self.x = x
        self.y = y
        self.some_other_param = some_other_param
        self.function = function

    def score(self) -> int:
        return self.function(self.x, self.y)

def test_score():
    def test_function(x, y):
        return x + y

    # Test case 1: x = 0, y = 0
    problem1 = SearchProblem(0, 0, 1, test_function)
    assert problem1.score() == 0

    # Test case 2: x = 5, y = 7
    problem2 = SearchProblem(5, 7, 1, test_function)
    assert problem2.score() == 12

    # Additional test case: x = 3, y = 4
    problem3 = SearchProblem(3, 4, 1, test_function)
    assert problem3.score() == 7
