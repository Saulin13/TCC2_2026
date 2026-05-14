import sys
import os
sys.path.append(r'C:\Users\diogo\OneDrive\Área de Trabalho\Diogo\PUC\8 Periodo\TCC\TCC2_2026/repos/Python')
from graphs.bidirectional_breadth_first_search import search
import os
import sys




import pytest
from unittest.mock import MagicMock

def test_search():
    # Mocking the BFS objects and their methods
    fwd_bfs_mock = MagicMock()
    bwd_bfs_mock = MagicMock()

    # Setting up initial conditions for the test
    fwd_bfs_mock.node_queue = [MagicMock(pos=1), MagicMock(pos=2)]
    bwd_bfs_mock.node_queue = [MagicMock(pos=3), MagicMock(pos=4)]
    fwd_bfs_mock.get_successors.side_effect = lambda node: [MagicMock(pos=node.pos + 1)]
    bwd_bfs_mock.get_successors.side_effect = lambda node: [MagicMock(pos=node.pos - 1)]

    # Creating an instance of the class containing the search method
    search_instance = MagicMock()
    search_instance.fwd_bfs = fwd_bfs_mock
    search_instance.bwd_bfs = bwd_bfs_mock
    search_instance.reached = False
    search_instance.retrace_bidirectional_path = MagicMock(return_value="path")

    # Test when paths meet
    fwd_bfs_mock.node_queue[0].pos = 5
    bwd_bfs_mock.node_queue[0].pos = 5
    result = search_instance.search()
    assert result == "path"
    assert search_instance.reached is True

    # Test when paths do not meet
    fwd_bfs_mock.node_queue[0].pos = 1
    bwd_bfs_mock.node_queue[0].pos = 3
    search_instance.reached = False
    result = search_instance.search()
    assert result == [fwd_bfs_mock.start.pos]
    assert search_instance.reached is False
