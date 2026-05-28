import pytest
from cellular_automata.conways_game_of_life import new_generation

def test_new_generation_blinker():
    # Blinker pattern (oscillator)
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

def test_new_generation_block():
    # Block pattern (still life)
    initial_state = [
        [1, 1],
        [1, 1]
    ]
    expected_next_state = [
        [1, 1],
        [1, 1]
    ]
    assert new_generation(initial_state) == expected_next_state

def test_new_generation_empty():
    # Empty grid
    initial_state = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    expected_next_state = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    assert new_generation(initial_state) == expected_next_state

def test_new_generation_single_cell():
    # Single live cell (should die)
    initial_state = [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]
    expected_next_state = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    assert new_generation(initial_state) == expected_next_state

def test_new_generation_edge_case():
    # Edge case with a live cell at the corner
    initial_state = [
        [1, 0],
        [0, 0]
    ]
    expected_next_state = [
        [0, 0],
        [0, 0]
    ]
    assert new_generation(initial_state) == expected_next_state

def test_new_generation_invalid_input():
    # Invalid input case (non-integer values)
    initial_state = [
        [0, 1, 'a'],
        [1, 0, 1],
        [0, 1, 0]
    ]
    with pytest.raises(TypeError):
        new_generation(initial_state)