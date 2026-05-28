import pytest
import numpy as np
from scipy import sparse
from sklearn.utils.graph import single_source_shortest_path_length


def test_simple_path_graph():
    """Test with a simple linear path graph."""
    graph = np.array([
        [0, 1, 0, 0],
        [1, 0, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0]
    ])
    result = single_source_shortest_path_length(graph, 0)
    assert result == {0: 0, 1: 1, 2: 2}


def test_fully_connected_graph():
    """Test with a fully connected graph."""
    graph = np.ones((6, 6))
    result = single_source_shortest_path_length(graph, 2)
    assert result == {0: 1, 1: 1, 2: 0, 3: 1, 4: 1, 5: 1}


def test_disconnected_graph():
    """Test with a graph that has disconnected components."""
    graph = np.array([
        [0, 1, 0, 0],
        [1, 0, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0]
    ])
    result = single_source_shortest_path_length(graph, 0)
    assert result == {0: 0, 1: 1}


def test_single_node_graph():
    """Test with a single node graph."""
    graph = np.array([[0]])
    result = single_source_shortest_path_length(graph, 0)
    assert result == {0: 0}


def test_with_cutoff():
    """Test with cutoff parameter limiting search depth."""
    graph = np.array([
        [0, 1, 0, 0, 0],
        [1, 0, 1, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1],
        [0, 0, 0, 1, 0]
    ])
    result = single_source_shortest_path_length(graph, 0, cutoff=2)
    assert result == {0: 0, 1: 1, 2: 2}


def test_with_cutoff_zero():
    """Test with cutoff=0, should only return source node."""
    graph = np.array([
        [0, 1, 1],
        [1, 0, 1],
        [1, 1, 0]
    ])
    result = single_source_shortest_path_length(graph, 0, cutoff=0)
    assert result == {0: 0}


def test_sparse_csr_matrix():
    """Test with sparse CSR matrix input."""
    graph = sparse.csr_matrix(np.array([
        [0, 1, 0, 0],
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [0, 0, 1, 0]
    ]))
    result = single_source_shortest_path_length(graph, 0)
    assert result == {0: 0, 1: 1, 2: 2, 3: 3}


def test_sparse_lil_matrix():
    """Test with sparse LIL matrix input."""
    graph = sparse.lil_matrix(np.array([
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0]
    ]))
    result = single_source_shortest_path_length(graph, 1)
    assert result == {0: 1, 1: 0, 2: 1}


def test_directed_graph():
    """Test with a directed graph (asymmetric adjacency matrix)."""
    graph = np.array([
        [0, 1, 0],
        [0, 0, 1],
        [0, 0, 0]
    ])
    result = single_source_shortest_path_length(graph, 0)
    assert result == {0: 0, 1: 1, 2: 2}


def test_cycle_graph():
    """Test with a cycle graph."""
    graph = np.array([
        [0, 1, 0, 1],
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [1, 0, 1, 0]
    ])
    result = single_source_shortest_path_length(graph, 0)
    assert result == {0: 0, 1: 1, 2: 2, 3: 1}


def test_star_graph():
    """Test with a star graph (one central node connected to all others)."""
    graph = np.array([
        [0, 1, 1, 1],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0]
    ])
    result = single_source_shortest_path_length(graph, 0)
    assert result == {0: 0, 1: 1, 2: 1, 3: 1}


def test_different_source_node():
    """Test starting from a different source node."""
    graph = np.array([
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0]
    ])
    result = single_source_shortest_path_length(graph, 2)
    assert result == {0: 2, 1: 1, 2: 0}


def test_empty_neighbors():
    """Test with a node that has no neighbors."""
    graph = np.array([
        [0, 0, 0],
        [0, 0, 1],
        [0, 1, 0]
    ])
    result = single_source_shortest_path_length(graph, 0)
    assert result == {0: 0}