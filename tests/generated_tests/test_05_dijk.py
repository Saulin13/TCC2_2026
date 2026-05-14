import sys
import os
sys.path.append(r'C:\Users\diogo\OneDrive\Área de Trabalho\Diogo\PUC\8 Periodo\TCC\TCC2_2026/repos/Python')
from graphs.basic_graphs import dijk
import os
import sys




import pytest

def test_dijk():
    graph = {
        1: [(2, 7), (3, 9), (6, 14)],
        2: [(1, 7), (3, 10), (4, 15)],
        3: [(1, 9), (2, 10), (4, 11), (6, 2)],
        4: [(2, 15), (3, 11), (5, 6)],
        5: [(4, 6), (6, 9)],
        6: [(1, 14), (3, 2), (5, 9)]
    }
    start_node = 1
    expected_output = [7, 9, 20, 20]

    def capture_output(func, *args, **kwargs):
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        func(*args, **kwargs)
        sys.stdout = sys.__stdout__
        return captured_output.getvalue().strip().split('\n')

    output = capture_output(dijk, graph, start_node)
    output = list(map(int, output))
    
    assert output == expected_output

if __name__ == "__main__":
    pytest.main()
