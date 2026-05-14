import sys
import os
sys.path.append(r'C:\Users\diogo\OneDrive\Área de Trabalho\Diogo\PUC\8 Periodo\TCC\TCC2_2026/repos/Python')
from graphs.minimum_spanning_tree_prims2 import prims_algo
import os
import sys




import pytest
from sys import maxsize

class GraphUndirectedWeighted:
    def __init__(self):
        self.connections = {}

    def add_edge(self, node1, node2, weight):
        if node1 not in self.connections:
            self.connections[node1] = {}
        if node2 not in self.connections:
            self.connections[node2] = {}
        self.connections[node1][node2] = weight
        self.connections[node2][node1] = weight

class MinPriorityQueue:
    def __init__(self):
        self.queue = []

    def push(self, node, weight):
        self.queue.append((weight, node))
        self.queue.sort()

    def extract_min(self):
        return self.queue.pop(0)[1]

    def update_key(self, node, new_weight):
        for i, (weight, n) in enumerate(self.queue):
            if n == node:
                self.queue[i] = (new_weight, node)
                break
        self.queue.sort()

    def is_empty(self):
        return len(self.queue) == 0

def test_prims_algo():
    graph = GraphUndirectedWeighted()
    graph.add_edge("a", "b", 3)
    graph.add_edge("b", "c", 10)
    graph.add_edge("c", "d", 5)
    graph.add_edge("a", "c", 15)
    graph.add_edge("b", "d", 100)

    dist, parent = prims_algo(graph)

    assert abs(dist["a"] - dist["b"]) == 3
    assert abs(dist["d"] - dist["b"]) == 15
    assert abs(dist["a"] - dist["c"]) == 13
