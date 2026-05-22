import pytest
from graphs.basic_graphs import floy

def test_floy_normal_case():
    a = [
        [0, 3, float('inf'), 7],
        [8, 0, 2, float('inf')],
        [5, float('inf'), 0, 1],
        [2, float('inf'), float('inf'), 0]
    ]
    n = 4
    expected_output = [
        [0, 3, 5, 6],
        [5, 0, 2, 3],
        [3, 6, 0, 1],
        [2, 5, 7, 0]
    ]
    assert floy((a, n)) == expected_output

def test_floy_single_node():
    a = [[0]]
    n = 1
    expected_output = [[0]]
    assert floy((a, n)) == expected_output

def test_floy_no_path():
    a = [
        [0, float('inf')],
        [float('inf'), 0]
    ]
    n = 2
    expected_output = [
        [0, float('inf')],
        [float('inf'), 0]
    ]
    assert floy((a, n)) == expected_output

def test_floy_negative_cycle():
    a = [
        [0, 1, float('inf')],
        [float('inf'), 0, -1],
        [-1, float('inf'), 0]
    ]
    n = 3
    expected_output = [
        [0, 1, 0],
        [-1, 0, -1],
        [-2, -1, 0]
    ]
    assert floy((a, n)) == expected_output

def test_floy_invalid_input():
    a = [
        [0, 1],
        [1, 0, 2]
    ]
    n = 2
    with pytest.raises(IndexError):
        floy((a, n))