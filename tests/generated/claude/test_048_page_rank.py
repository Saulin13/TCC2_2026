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
    
    assert result == {"A": 0.15}


def test_page_rank_two_nodes_bidirectional():
    node_a = Node("A", inbound=["B"], outbound=["B"])
    node_b = Node("B", inbound=["A"], outbound=["A"])
    nodes = [node_a, node_b]
    
    result = page_rank(nodes, limit=1, d=0.85)
    
    assert result == {"A": 1.0, "B": 1.0}


def test_page_rank_three_nodes_linear():
    node_a = Node("A", inbound=[], outbound=["B"])
    node_b = Node("B", inbound=["A"], outbound=["C"])
    node_c = Node("C", inbound=["B"], outbound=[])
    nodes = [node_a, node_b, node_c]
    
    result = page_rank(nodes, limit=2, d=0.85)
    
    assert "A" in result
    assert "B" in result
    assert "C" in result
    assert result["A"] == 0.15
    assert abs(result["B"] - 0.2775) < 0.0001
    assert abs(result["C"] - 0.38625) < 0.0001


def test_page_rank_four_nodes_complex():
    node_a = Node("A", inbound=["B", "C"], outbound=["B", "C"])
    node_b = Node("B", inbound=["A", "D"], outbound=["A", "C"])
    node_c = Node("C", inbound=["A", "B"], outbound=["D"])
    node_d = Node("D", inbound=["C"], outbound=["B"])
    nodes = [node_a, node_b, node_c, node_d]
    
    result = page_rank(nodes, limit=3, d=0.85)
    
    assert len(result) == 4
    assert all(key in result for key in ["A", "B", "C", "D"])
    assert all(isinstance(val, (int, float)) for val in result.values())
    assert all(val > 0 for val in result.values())


def test_page_rank_default_parameters():
    node_a = Node("A", inbound=["B"], outbound=["B"])
    node_b = Node("B", inbound=["A"], outbound=["A"])
    nodes = [node_a, node_b]
    
    result = page_rank(nodes)
    
    assert result == {"A": 1.0, "B": 1.0}


def test_page_rank_custom_damping_factor():
    node_a = Node("A", inbound=[], outbound=["B"])
    node_b = Node("B", inbound=["A"], outbound=[])
    nodes = [node_a, node_b]
    
    result = page_rank(nodes, limit=1, d=0.5)
    
    assert result["A"] == 0.5
    assert result["B"] == 1.0


def test_page_rank_zero_iterations():
    node_a = Node("A", inbound=[], outbound=["B"])
    node_b = Node("B", inbound=["A"], outbound=[])
    nodes = [node_a, node_b]
    
    result = page_rank(nodes, limit=0, d=0.85)
    
    assert result == {"A": 1, "B": 1}


def test_page_rank_multiple_inbound_links():
    node_a = Node("A", inbound=["B", "C", "D"], outbound=["B"])
    node_b = Node("B", inbound=["A"], outbound=["A", "C", "D"])
    node_c = Node("C", inbound=["B"], outbound=["A"])
    node_d = Node("D", inbound=["B"], outbound=["A"])
    nodes = [node_a, node_b, node_c, node_d]
    
    result = page_rank(nodes, limit=2, d=0.85)
    
    assert len(result) == 4
    assert result["A"] > result["B"]


def test_page_rank_empty_list():
    nodes = []
    
    result = page_rank(nodes, limit=3, d=0.85)
    
    assert result == {}


def test_page_rank_node_with_zero_outbound():
    node_a = Node("A", inbound=[], outbound=[])
    node_b = Node("B", inbound=[], outbound=[])
    nodes = [node_a, node_b]
    
    result = page_rank(nodes, limit=1, d=0.85)
    
    assert result == {"A": 0.15, "B": 0.15}


def test_page_rank_division_by_zero_protection():
    node_a = Node("A", inbound=["B"], outbound=["B"])
    node_b = Node("B", inbound=["A"], outbound=[])
    nodes = [node_a, node_b]
    
    with pytest.raises(ZeroDivisionError):
        page_rank(nodes, limit=1, d=0.85)