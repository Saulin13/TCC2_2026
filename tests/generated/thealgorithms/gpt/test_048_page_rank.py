import pytest
from graphs.page_rank import page_rank

class Node:
    def __init__(self, name, inbound=None, outbound=None):
        self.name = name
        self.inbound = inbound if inbound else []
        self.outbound = outbound if outbound else []

def test_page_rank_normal_case():
    node_a = Node('A', inbound=['B', 'C'], outbound=['B', 'C'])
    node_b = Node('B', inbound=['A'], outbound=['A', 'C'])
    node_c = Node('C', inbound=['A'], outbound=['A'])
    nodes = [node_a, node_b, node_c]
    
    expected_ranks = {'A': 1.0, 'B': 1.0, 'C': 1.0}  # Example expected output
    ranks = page_rank(nodes)
    assert ranks == expected_ranks

def test_page_rank_single_node():
    node_a = Node('A', inbound=[], outbound=[])
    nodes = [node_a]
    
    expected_ranks = {'A': 1.0}
    ranks = page_rank(nodes)
    assert ranks == expected_ranks

def test_page_rank_disconnected_graph():
    node_a = Node('A', inbound=[], outbound=[])
    node_b = Node('B', inbound=[], outbound=[])
    nodes = [node_a, node_b]
    
    expected_ranks = {'A': 1.0, 'B': 1.0}
    ranks = page_rank(nodes)
    assert ranks == expected_ranks

def test_page_rank_no_outbound_links():
    node_a = Node('A', inbound=['B'], outbound=[])
    node_b = Node('B', inbound=['A'], outbound=[])
    nodes = [node_a, node_b]
    
    expected_ranks = {'A': 1.0, 'B': 1.0}
    ranks = page_rank(nodes)
    assert ranks == expected_ranks

def test_page_rank_zero_iterations():
    node_a = Node('A', inbound=['B'], outbound=['B'])
    node_b = Node('B', inbound=['A'], outbound=['A'])
    nodes = [node_a, node_b]
    
    expected_ranks = {'A': 1.0, 'B': 1.0}
    ranks = page_rank(nodes, limit=0)
    assert ranks == expected_ranks

def test_page_rank_invalid_node_structure():
    with pytest.raises(AttributeError):
        page_rank([{'name': 'A', 'inbound': [], 'outbound': []}])