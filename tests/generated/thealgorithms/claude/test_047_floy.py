import pytest
from graphs.basic_graphs import floy


def test_floy_simple_graph():
    n = 3
    INF = float('inf')
    a = [
        [0, 5, INF],
        [50, 0, 15],
        [30, INF, 0]
    ]
    result = floy((a, n))
    expected_dist = [
        [0, 5, 20],
        [45, 0, 15],
        [30, 35, 0]
    ]
    assert a == expected_dist


def test_floy_four_nodes():
    n = 4
    INF = float('inf')
    a = [
        [0, 3, INF, 7],
        [8, 0, 2, INF],
        [5, INF, 0, 1],
        [2, INF, INF, 0]
    ]
    result = floy((a, n))
    expected_dist = [
        [0, 3, 5, 6],
        [7, 0, 2, 3],
        [3, 6, 0, 1],
        [2, 5, 7, 0]
    ]
    assert a == expected_dist


def test_floy_single_node():
    n = 1
    a = [[0]]
    result = floy((a, n))
    expected_dist = [[0]]
    assert a == expected_dist


def test_floy_two_nodes_connected():
    n = 2
    a = [
        [0, 10],
        [20, 0]
    ]
    result = floy((a, n))
    expected_dist = [
        [0, 10],
        [20, 0]
    ]
    assert a == expected_dist


def test_floy_disconnected_graph():
    n = 3
    INF = float('inf')
    a = [
        [0, 1, INF],
        [INF, 0, INF],
        [INF, INF, 0]
    ]
    result = floy((a, n))
    expected_dist = [
        [0, 1, INF],
        [INF, 0, INF],
        [INF, INF, 0]
    ]
    assert a == expected_dist


def test_floy_all_connected():
    n = 3
    a = [
        [0, 1, 4],
        [1, 0, 2],
        [4, 2, 0]
    ]
    result = floy((a, n))
    expected_dist = [
        [0, 1, 3],
        [1, 0, 2],
        [3, 2, 0]
    ]
    assert a == expected_dist


def test_floy_with_negative_weights():
    n = 3
    a = [
        [0, -1, 4],
        [float('inf'), 0, 3],
        [float('inf'), float('inf'), 0]
    ]
    result = floy((a, n))
    expected_dist = [
        [0, -1, 2],
        [float('inf'), 0, 3],
        [float('inf'), float('inf'), 0]
    ]
    assert a == expected_dist


def test_floy_empty_tuple_raises_error():
    with pytest.raises((ValueError, TypeError)):
        floy(())


def test_floy_invalid_input_raises_error():
    with pytest.raises((TypeError, AttributeError)):
        floy(None)


def test_floy_mismatched_dimensions():
    n = 2
    a = [
        [0, 1, 2],
        [3, 0, 4]
    ]
    with pytest.raises(IndexError):
        floy((a, n))