import pytest
from graphs.graphs_floyd_warshall import floyd_warshall

def test_floyd_warshall_normal_case():
    graph = [
        [0, 3, float('inf'), 7],
        [8, 0, 2, float('inf')],
        [5, float('inf'), 0, 1],
        [2, float('inf'), float('inf'), 0]
    ]
    expected = [
        [0, 3, 5, 6],
        [5, 0, 2, 3],
        [3, 6, 0, 1],
        [2, 5, 7, 0]
    ]
    result, _ = floyd_warshall(graph, 4)
    assert result == expected

def test_floyd_warshall_single_vertex():
    graph = [[0]]
    expected = [[0]]
    result, _ = floyd_warshall(graph, 1)
    assert result == expected

def test_floyd_warshall_no_edges():
    graph = [
        [0, float('inf')],
        [float('inf'), 0]
    ]
    expected = [
        [0, float('inf')],
        [float('inf'), 0]
    ]
    result, _ = floyd_warshall(graph, 2)
    assert result == expected

def test_floyd_warshall_negative_cycle():
    graph = [
        [0, 1, float('inf')],
        [float('inf'), 0, -1],
        [-1, float('inf'), 0]
    ]
    expected = [
        [0, 1, 0],
        [-1, 0, -1],
        [-2, -1, 0]
    ]
    result, _ = floyd_warshall(graph, 3)
    assert result == expected

def test_floyd_warshall_invalid_graph():
    graph = [
        [0, 1],
        [1, 0, 2]  # Invalid row length
    ]
    with pytest.raises(IndexError):
        floyd_warshall(graph, 2)