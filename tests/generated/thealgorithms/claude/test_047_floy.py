import pytest
from graphs.basic_graphs import floy


def test_floy_simple_graph():
    n = 3
    INF = float('inf')
    a = [
        [0, 5, INF],
        [INF, 0, 3],
        [INF, INF, 0]
    ]
    result = floy((a, n))
    assert a[0][0] == 0
    assert a[0][1] == 5
    assert a[0][2] == 8
    assert a[1][0] == INF
    assert a[1][1] == 0
    assert a[1][2] == 3


def test_floy_fully_connected_graph():
    n = 3
    a = [
        [0, 4, 2],
        [4, 0, 3],
        [2, 3, 0]
    ]
    result = floy((a, n))
    assert a[0][0] == 0
    assert a[0][1] == 4
    assert a[0][2] == 2
    assert a[1][0] == 4
    assert a[1][1] == 0
    assert a[1][2] == 3
    assert a[2][0] == 2
    assert a[2][1] == 3
    assert a[2][2] == 0


def test_floy_with_shorter_path():
    n = 4
    INF = float('inf')
    a = [
        [0, 3, INF, 7],
        [8, 0, 2, INF],
        [5, INF, 0, 1],
        [2, INF, INF, 0]
    ]
    result = floy((a, n))
    assert a[0][0] == 0
    assert a[0][1] == 3
    assert a[0][2] == 5
    assert a[0][3] == 6
    assert a[1][0] == 7
    assert a[1][1] == 0
    assert a[1][2] == 2
    assert a[1][3] == 3


def test_floy_single_node():
    n = 1
    a = [[0]]
    result = floy((a, n))
    assert a[0][0] == 0


def test_floy_two_nodes_connected():
    n = 2
    a = [
        [0, 5],
        [3, 0]
    ]
    result = floy((a, n))
    assert a[0][0] == 0
    assert a[0][1] == 5
    assert a[1][0] == 3
    assert a[1][1] == 0


def test_floy_disconnected_graph():
    n = 3
    INF = float('inf')
    a = [
        [0, 1, INF],
        [1, 0, INF],
        [INF, INF, 0]
    ]
    result = floy((a, n))
    assert a[0][0] == 0
    assert a[0][1] == 1
    assert a[0][2] == INF
    assert a[1][0] == 1
    assert a[1][1] == 0
    assert a[1][2] == INF
    assert a[2][0] == INF
    assert a[2][1] == INF
    assert a[2][2] == 0


def test_floy_with_negative_weights():
    n = 3
    a = [
        [0, -1, 4],
        [float('inf'), 0, 3],
        [float('inf'), float('inf'), 0]
    ]
    result = floy((a, n))
    assert a[0][0] == 0
    assert a[0][1] == -1
    assert a[0][2] == 2
    assert a[1][1] == 0
    assert a[1][2] == 3


def test_floy_empty_graph():
    n = 0
    a = []
    result = floy((a, n))
    assert len(a) == 0


def test_floy_modifies_input_matrix():
    n = 2
    INF = float('inf')
    a = [
        [0, INF],
        [INF, 0]
    ]
    original_value = a[0][1]
    result = floy((a, n))
    assert a[0][1] == original_value