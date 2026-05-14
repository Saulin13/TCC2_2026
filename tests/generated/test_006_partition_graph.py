import pytest
from graphs.karger import partition_graph

def test_partition_graph_simple():
    graph = {'0': ['1'], '1': ['0']}
    result = partition_graph(graph)
    assert result == {('0', '1')} or result == {('1', '0')}

def test_partition_graph_triangle():
    graph = {'0': ['1', '2'], '1': ['0', '2'], '2': ['0', '1']}
    result = partition_graph(graph)
    assert len(result) == 1
    assert any(edge in result for edge in [('0', '1'), ('1', '2'), ('2', '0')])

def test_partition_graph_square():
    graph = {'0': ['1', '3'], '1': ['0', '2'], '2': ['1', '3'], '3': ['0', '2']}
    result = partition_graph(graph)
    assert len(result) == 2
    assert any(edge in result for edge in [('0', '1'), ('1', '2'), ('2', '3'), ('3', '0')])

def test_partition_graph_disconnected():
    graph = {'0': [], '1': []}
    result = partition_graph(graph)
    assert result == set()

def test_partition_graph_single_node():
    graph = {'0': []}
    result = partition_graph(graph)
    assert result == set()

def test_partition_graph_no_edges():
    graph = {'0': [], '1': [], '2': []}
    result = partition_graph(graph)
    assert result == set()

def test_partition_graph_invalid_input():
    with pytest.raises(KeyError):
        graph = {'0': ['1'], '1': ['2']}
        partition_graph(graph)