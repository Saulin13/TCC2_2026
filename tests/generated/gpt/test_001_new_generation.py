import pytest
from cellular_automata.conways_game_of_life import new_generation

def test_new_generation_blinker():
    blinker = [
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0]
    ]
    expected = [
        [0, 0, 0],
        [1, 1, 1],
        [0, 0, 0]
    ]
    assert new_generation(blinker) == expected

def test_new_generation_block():
    block = [
        [1, 1],
        [1, 1]
    ]
    expected = [
        [1, 1],
        [1, 1]
    ]
    assert new_generation(block) == expected

def test_new_generation_empty():
    empty = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    expected = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    assert new_generation(empty) == expected

def test_new_generation_single_cell():
    single_cell = [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]
    expected = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    assert new_generation(single_cell) == expected

def test_new_generation_edge_case():
    edge_case = [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ]
    expected = [
        [1, 0, 1],
        [0, 0, 0],
        [1, 0, 1]
    ]
    assert new_generation(edge_case) == expected

def test_new_generation_invalid_input():
    with pytest.raises(TypeError):
        new_generation(None)