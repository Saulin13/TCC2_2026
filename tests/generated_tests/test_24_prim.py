import sys
import os
sys.path.append(r'C:\Users\diogo\OneDrive\Área de Trabalho\Diogo\PUC\8 Periodo\TCC\TCC2_2026/repos/Python')
from graphs.basic_graphs import prim
import os
import sys




import pytest

def test_prim():
    # Grafo de exemplo
    g = {
        'A': [('B', 1), ('C', 4)],
        'B': [('A', 1), ('C', 2), ('D', 5)],
        'C': [('A', 4), ('B', 2), ('D', 1)],
        'D': [('B', 5), ('C', 1)]
    }
    
    # Teste para o grafo acima começando no vértice 'A'
    result = prim(g, 'A')
    expected = {'A': 0, 'B': 1, 'C': 2, 'D': 1}
    assert result == expected

    # Teste para o grafo acima começando no vértice 'B'
    result = prim(g, 'B')
    expected = {'B': 0, 'A': 1, 'C': 2, 'D': 1}
    assert result == expected

    # Teste para o grafo acima começando no vértice 'C'
    result = prim(g, 'C')
    expected = {'C': 0, 'B': 2, 'D': 1, 'A': 1}
    assert result == expected

    # Teste para o grafo acima começando no vértice 'D'
    result = prim(g, 'D')
    expected = {'D': 0, 'C': 1, 'B': 2, 'A': 1}
    assert result == expected

if __name__ == "__main__":
    pytest.main()
