import pytest
from graphs.graphs_floyd_warshall import floyd_warshall


def test_floyd_warshall_simple_graph():
    graph = [
        [0, 5, float('inf'), 10],
        [float('inf'), 0, 3, float('inf')],
        [float('inf'), float('inf'), 0, 1],
        [float('inf'), float('inf'), float('inf'), 0]
    ]
    v = 4
    dist, returned_v = floyd_warshall(graph, v)
    
    assert returned_v == 4
    assert dist[0][0] == 0
    assert dist[0][1] == 5
    assert dist[0][2] == 8
    assert dist[0][3] == 9
    assert dist[1][1] == 0
    assert dist[1][2] == 3
    assert dist[1][3] == 4
    assert dist[2][2] == 0
    assert dist[2][3] == 1
    assert dist[3][3] == 0


def test_floyd_warshall_single_vertex():
    graph = [[0]]
    v = 1
    dist, returned_v = floyd_warshall(graph, v)
    
    assert returned_v == 1
    assert dist[0][0] == 0


def test_floyd_warshall_two_vertices_connected():
    graph = [
        [0, 7],
        [float('inf'), 0]
    ]
    v = 2
    dist, returned_v = floyd_warshall(graph, v)
    
    assert returned_v == 2
    assert dist[0][0] == 0
    assert dist[0][1] == 7
    assert dist[1][0] == float('inf')
    assert dist[1][1] == 0


def test_floyd_warshall_fully_connected_graph():
    graph = [
        [0, 3, 8],
        [2, 0, 5],
        [4, 1, 0]
    ]
    v = 3
    dist, returned_v = floyd_warshall(graph, v)
    
    assert returned_v == 3
    assert dist[0][0] == 0
    assert dist[0][1] == 3
    assert dist[0][2] == 8
    assert dist[1][0] == 2
    assert dist[1][1] == 0
    assert dist[1][2] == 5
    assert dist[2][0] == 3
    assert dist[2][1] == 1
    assert dist[2][2] == 0


def test_floyd_warshall_disconnected_graph():
    graph = [
        [0, float('inf'), float('inf')],
        [float('inf'), 0, float('inf')],
        [float('inf'), float('inf'), 0]
    ]
    v = 3
    dist, returned_v = floyd_warshall(graph, v)
    
    assert returned_v == 3
    assert dist[0][0] == 0
    assert dist[0][1] == float('inf')
    assert dist[0][2] == float('inf')
    assert dist[1][0] == float('inf')
    assert dist[1][1] == 0
    assert dist[1][2] == float('inf')
    assert dist[2][0] == float('inf')
    assert dist[2][1] == float('inf')
    assert dist[2][2] == 0


def test_floyd_warshall_with_intermediate_paths():
    graph = [
        [0, 1, float('inf'), float('inf')],
        [float('inf'), 0, 1, float('inf')],
        [float('inf'), float('inf'), 0, 1],
        [float('inf'), float('inf'), float('inf'), 0]
    ]
    v = 4
    dist, returned_v = floyd_warshall(graph, v)
    
    assert returned_v == 4
    assert dist[0][3] == 3
    assert dist[0][2] == 2
    assert dist[1][3] == 2


def test_floyd_warshall_zero_vertices():
    graph = []
    v = 0
    dist, returned_v = floyd_warshall(graph, v)
    
    assert returned_v == 0
    assert dist == []


def test_floyd_warshall_with_weights():
    graph = [
        [0, 4, float('inf'), 5],
        [float('inf'), 0, 1, float('inf')],
        [2, float('inf'), 0, 3],
        [float('inf'), float('inf'), float('inf'), 0]
    ]
    v = 4
    dist, returned_v = floyd_warshall(graph, v)
    
    assert returned_v == 4
    assert dist[0][0] == 0
    assert dist[0][1] == 4
    assert dist[0][2] == 5
    assert dist[0][3] == 5
    assert dist[2][1] == 6