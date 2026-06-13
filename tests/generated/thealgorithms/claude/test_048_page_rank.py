import pytest
from graphs.page_rank import page_rank


class Node:
    def __init__(self, name, inbound=None, outbound=None):
        self.name = name
        self.inbound = inbound if inbound is not None else []
        self.outbound = outbound if outbound is not None else []


def test_page_rank_single_node():
    node_a = Node("A", inbound=[], outbound=[])
    nodes = [node_a]
    
    result = page_rank(nodes, limit=1, d=0.85)
    
    assert result is None


def test_page_rank_two_nodes_bidirectional():
    node_a = Node("A", inbound=["B"], outbound=["B"])
    node_b = Node("B", inbound=["A"], outbound=["A"])
    nodes = [node_a, node_b]
    
    result = page_rank(nodes, limit=1, d=0.85)
    
    assert result is None


def test_page_rank_three_nodes_linear():
    node_a = Node("A", inbound=[], outbound=["B"])
    node_b = Node("B", inbound=["A"], outbound=["C"])
    node_c = Node("C", inbound=["B"], outbound=[])
    nodes = [node_a, node_b, node_c]
    
    result = page_rank(nodes, limit=2, d=0.85)
    
    assert result is None


def test_page_rank_circular_graph():
    node_a = Node("A", inbound=["C"], outbound=["B"])
    node_b = Node("B", inbound=["A"], outbound=["C"])
    node_c = Node("C", inbound=["B"], outbound=["A"])
    nodes = [node_a, node_b, node_c]
    
    result = page_rank(nodes, limit=3, d=0.85)
    
    assert result is None


def test_page_rank_hub_and_spoke():
    node_hub = Node("Hub", inbound=["A", "B", "C"], outbound=["A", "B", "C"])
    node_a = Node("A", inbound=["Hub"], outbound=["Hub"])
    node_b = Node("B", inbound=["Hub"], outbound=["Hub"])
    node_c = Node("C", inbound=["Hub"], outbound=["Hub"])
    nodes = [node_hub, node_a, node_b, node_c]
    
    result = page_rank(nodes, limit=3, d=0.85)
    
    assert result is None


def test_page_rank_default_parameters():
    node_a = Node("A", inbound=["B"], outbound=["B"])
    node_b = Node("B", inbound=["A"], outbound=["A"])
    nodes = [node_a, node_b]
    
    result = page_rank(nodes)
    
    assert result is None


def test_page_rank_zero_iterations():
    node_a = Node("A", inbound=[], outbound=[])
    nodes = [node_a]
    
    result = page_rank(nodes, limit=0, d=0.85)
    
    assert result is None


def test_page_rank_different_damping_factor():
    node_a = Node("A", inbound=["B"], outbound=["B"])
    node_b = Node("B", inbound=["A"], outbound=["A"])
    nodes = [node_a, node_b]
    
    result = page_rank(nodes, limit=2, d=0.5)
    
    assert result is None


def test_page_rank_node_with_no_outbound():
    node_a = Node("A", inbound=[], outbound=["B"])
    node_b = Node("B", inbound=["A"], outbound=[])
    nodes = [node_a, node_b]
    
    result = page_rank(nodes, limit=2, d=0.85)
    
    assert result is None


def test_page_rank_complex_graph():
    node_a = Node("A", inbound=["C", "D"], outbound=["B", "C"])
    node_b = Node("B", inbound=["A"], outbound=["C"])
    node_c = Node("C", inbound=["A", "B"], outbound=["A"])
    node_d = Node("D", inbound=[], outbound=["A"])
    nodes = [node_a, node_b, node_c, node_d]
    
    result = page_rank(nodes, limit=5, d=0.85)
    
    assert result is None


def test_page_rank_empty_nodes_list():
    nodes = []
    
    result = page_rank(nodes, limit=3, d=0.85)
    
    assert result is None


def test_page_rank_node_with_self_reference():
    node_a = Node("A", inbound=["A"], outbound=["A"])
    nodes = [node_a]
    
    with pytest.raises(ZeroDivisionError):
        page_rank(nodes, limit=1, d=0.85)


def test_page_rank_missing_inbound_reference():
    node_a = Node("A", inbound=["NonExistent"], outbound=["B"])
    node_b = Node("B", inbound=["A"], outbound=["A"])
    nodes = [node_a, node_b]
    
    with pytest.raises(KeyError):
        page_rank(nodes, limit=1, d=0.85)