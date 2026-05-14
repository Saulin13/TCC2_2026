import pytest
from graphs.basic_graphs import dijk

def test_dijk_normal_case():
    graph = {
        1: [(2, 7), (3, 9), (6, 14)],
        2: [(1, 7), (3, 10), (4, 15)],
        3: [(1, 9), (2, 10), (4, 11), (6, 2)],
        4: [(2, 15), (3, 11), (5, 6)],
        5: [(4, 6), (6, 9)],
        6: [(1, 14), (3, 2), (5, 9)]
    }
    # Expected output distances from node 1 to others
    expected_output = [7, 9, 20, 20]
    assert dijk(graph, 1) == expected_output

def test_dijk_single_node():
    graph = {1: []}
    # No other nodes to reach, so no distances to print
    expected_output = []
    assert dijk(graph, 1) == expected_output

def test_dijk_disconnected_graph():
    graph = {
        1: [(2, 1)],
        2: [(1, 1)],
        3: [(4, 1)],
        4: [(3, 1)]
    }
    # Nodes 3 and 4 are disconnected from 1, so they should not appear in the output
    expected_output = [1]
    assert dijk(graph, 1) == expected_output

def test_dijk_no_edges():
    graph = {
        1: [],
        2: [],
        3: []
    }
    # No edges, so no distances to print
    expected_output = []
    assert dijk(graph, 1) == expected_output

def test_dijk_invalid_start_node():
    graph = {
        1: [(2, 7)],
        2: [(1, 7)]
    }
    with pytest.raises(KeyError):
        dijk(graph, 3)  # Start node 3 does not exist in the graph