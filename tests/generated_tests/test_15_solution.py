import sys
import os
sys.path.append(r'C:\Users\diogo\OneDrive\Área de Trabalho\Diogo\PUC\8 Periodo\TCC\TCC2_2026/repos/Python')
from project_euler.problem_067.sol2 import solution
import os
import sys




import pytest
from unittest.mock import mock_open, patch

# Mock data for the triangle.txt file
mock_triangle_data = """3
7 4
2 4 6
8 5 9 3"""

# The expected result for the mock data above
expected_result = 23

def test_solution():
    with patch("builtins.open", mock_open(read_data=mock_triangle_data)):
        with patch("os.path.dirname", return_value=""), patch("os.path.realpath", return_value=""):
              # Replace 'your_module' with the actual module name
            assert solution() == expected_result


Make sure to replace `'your_module'` with the actual name of the module where the `solution` function is defined.