import sys
import os
sys.path.append(r'C:\Users\diogo\OneDrive\Área de Trabalho\Diogo\PUC\8 Periodo\TCC\TCC2_2026/repos/Python')
from maths.simultaneous_linear_equation_solver import solve_simultaneous
import os
import sys




import pytest

def test_solve_simultaneous():
      # Replace 'your_module' with the actual module name

    # Test cases with expected results
    assert solve_simultaneous([[1, 2, 3], [4, 5, 6]]) == [-1.0, 2.0]
    assert solve_simultaneous([[0, -3, 1, 7], [3, 2, -1, 11], [5, 1, -2, 12]]) == [6.4, 1.2, 10.6]

    # Test cases expecting exceptions
    with pytest.raises(IndexError, match="solve_simultaneous() requires n lists of length n+1"):
        solve_simultaneous([])

    with pytest.raises(IndexError, match="solve_simultaneous() requires n lists of length n+1"):
        solve_simultaneous([[1, 2, 3], [1, 2]])

    with pytest.raises(ValueError, match="solve_simultaneous() requires lists of integers"):
        solve_simultaneous([[1, 2, 3], ["a", 7, 8]])

    with pytest.raises(ValueError, match="solve_simultaneous() requires at least 1 full equation"):
        solve_simultaneous([[0, 2, 3], [4, 0, 6]])

# Run the tests
if __name__ == "__main__":
    pytest.main()
