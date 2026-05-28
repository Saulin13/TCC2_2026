import pytest
from cellular_automata.conways_game_of_life import new_generation


def test_blinker_horizontal_to_vertical():
    cells = [
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0]
    ]
    expected = [
        [0, 0, 0],
        [1, 1, 1],
        [0, 0, 0]
    ]
    assert new_generation(cells) == expected


def test_blinker_vertical_to_horizontal():
    cells = [
        [0, 0, 0],
        [1, 1, 1],
        [0, 0, 0]
    ]
    expected = [
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0]
    ]
    assert new_generation(cells) == expected


def test_block_still_life():
    cells = [
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0]
    ]
    expected = [
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0]
    ]
    assert new_generation(cells) == expected


def test_all_dead_cells():
    cells = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    expected = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    assert new_generation(cells) == expected


def test_single_cell_dies():
    cells = [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]
    expected = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    assert new_generation(cells) == expected


def test_three_cells_create_new_cell():
    cells = [
        [1, 1, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]
    expected = [
        [1, 1, 0],
        [1, 1, 0],
        [0, 0, 0]
    ]
    assert new_generation(cells) == expected


def test_glider_first_step():
    cells = [
        [0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
    expected = [
        [0, 0, 0, 0, 0],
        [1, 0, 1, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
    assert new_generation(cells) == expected


def test_single_row():
    cells = [[1, 1, 1]]
    expected = [[0, 1, 0]]
    assert new_generation(cells) == expected


def test_single_column():
    cells = [[1], [1], [1]]
    expected = [[0], [1], [0]]
    assert new_generation(cells) == expected


def test_1x1_grid_alive():
    cells = [[1]]
    expected = [[0]]
    assert new_generation(cells) == expected


def test_1x1_grid_dead():
    cells = [[0]]
    expected = [[0]]
    assert new_generation(cells) == expected


def test_2x2_grid_all_alive():
    cells = [
        [1, 1],
        [1, 1]
    ]
    expected = [
        [1, 1],
        [1, 1]
    ]
    assert new_generation(cells) == expected


def test_overpopulation():
    cells = [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ]
    expected = [
        [1, 0, 1],
        [0, 0, 0],
        [1, 0, 1]
    ]
    assert new_generation(cells) == expected


def test_empty_grid():
    cells = []
    expected = []
    assert new_generation(cells) == expected


def test_rectangular_grid():
    cells = [
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0]
    ]
    expected = [
        [0, 0, 0, 0],
        [1, 1, 1, 0],
        [0, 0, 0, 0]
    ]
    assert new_generation(cells) == expected