import pytest
from graphs.page_rank import page_rank

class Node:
    def __init__(self, name, inbound=None, outbound=None):
        self.name = name
        self.inbound = inbound if inbound else []
        self.outbound = outbound if outbound else []

def test_page_rank_normal_case():
    node_a = Node("A", inbound=["B", "C"], outbound=["B", "C"])
    node_b = Node("B", inbound=["A"], outbound=["A"])
    node_c = Node("C", inbound=["A"], outbound=["A"])
    nodes = [node_a, node_b, node_c]
    
    result = page_rank(nodes, limit=10, d=0.85)
    assert isinstance(result, dict)
    assert set(result.keys()) == {"A", "B", "C"}
    assert all(isinstance(rank, float) for rank in result.values())

def test_page_rank_single_node():
    node_a = Node("A", inbound=[], outbound=[])
    nodes = [node_a]
    
    result = page_rank(nodes, limit=10, d=0.85)
    assert result == {"A": 1.0}

def test_page_rank_no_inbound():
    node_a = Node("A", inbound=[], outbound=["B"])
    node_b = Node("B", inbound=[], outbound=["A"])
    nodes = [node_a, node_b]
    
    result = page_rank(nodes, limit=10, d=0.85)
    assert result["A"] == pytest.approx(0.5, rel=1e-2)
    assert result["B"] == pytest.approx(0.5, rel=1e-2)

def test_page_rank_no_outbound():
    node_a = Node("A", inbound=["B"], outbound=[])
    node_b = Node("B", inbound=["A"], outbound=[])
    nodes = [node_a, node_b]
    
    result = page_rank(nodes, limit=10, d=0.85)
    assert result["A"] == pytest.approx(0.5, rel=1e-2)
    assert result["B"] == pytest.approx(0.5, rel=1e-2)

def test_page_rank_disconnected_graph():
    node_a = Node("A", inbound=[], outbound=[])
    node_b = Node("B", inbound=[], outbound=[])
    nodes = [node_a, node_b]
    
    result = page_rank(nodes, limit=10, d=0.85)
    assert result["A"] == 1.0
    assert result["B"] == 1.0

def test_page_rank_invalid_node():
    with pytest.raises(AttributeError):
        page_rank([{"name": "A", "inbound": [], "outbound": []}], limit=10, d=0.85)