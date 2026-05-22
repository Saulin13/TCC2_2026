import pytest
from cellular_automata.conways_game_of_life import new_generation

def test_new_generation_normal_case():
    initial_state = [
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0]
    ]
    expected_next_state = [
        [0, 0, 0],
        [1, 1, 1],
        [0, 0, 0]
    ]
    assert new_generation(initial_state) == expected_next_state

def test_new_generation_edge_case_empty_grid():
    initial_state = []
    expected_next_state = []
    assert new_generation(initial_state) == expected_next_state

def test_new_generation_edge_case_single_cell_alive():
    initial_state = [
        [1]
    ]
    expected_next_state = [
        [0]
    ]
    assert new_generation(initial_state) == expected_next_state

def test_new_generation_edge_case_single_cell_dead():
    initial_state = [
        [0]
    ]
    expected_next_state = [
        [0]
    ]
    assert new_generation(initial_state) == expected_next_state

def test_new_generation_failure_case_non_square_grid():
    initial_state = [
        [1, 0, 1],
        [0, 1, 0]
    ]
    expected_next_state = [
        [0, 1, 0],
        [0, 1, 0]
    ]
    assert new_generation(initial_state) == expected_next_state

def test_new_generation_failure_case_invalid_input():
    initial_state = [
        [1, 0, 2],
        [0, 1, 0]
    ]
    with pytest.raises(ValueError):
        new_generation(initial_state)