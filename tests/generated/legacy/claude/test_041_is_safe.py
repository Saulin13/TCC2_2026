import pytest
from backtracking.sudoku import is_safe


def test_is_safe_empty_grid():
    grid = [[0 for _ in range(9)] for _ in range(9)]
    assert is_safe(grid, 0, 0, 5) is True
    assert is_safe(grid, 4, 4, 9) is True
    assert is_safe(grid, 8, 8, 1) is True


def test_is_safe_duplicate_in_row():
    grid = [[0 for _ in range(9)] for _ in range(9)]
    grid[0][5] = 7
    assert is_safe(grid, 0, 0, 7) is False
    assert is_safe(grid, 0, 0, 3) is True


def test_is_safe_duplicate_in_column():
    grid = [[0 for _ in range(9)] for _ in range(9)]
    grid[5][0] = 4
    assert is_safe(grid, 0, 0, 4) is False
    assert is_safe(grid, 0, 0, 8) is True


def test_is_safe_duplicate_in_3x3_subgrid():
    grid = [[0 for _ in range(9)] for _ in range(9)]
    grid[1][1] = 6
    assert is_safe(grid, 0, 0, 6) is False
    assert is_safe(grid, 0, 2, 6) is False
    assert is_safe(grid, 2, 2, 6) is False
    assert is_safe(grid, 0, 0, 2) is True


def test_is_safe_middle_subgrid():
    grid = [[0 for _ in range(9)] for _ in range(9)]
    grid[4][4] = 9
    assert is_safe(grid, 3, 3, 9) is False
    assert is_safe(grid, 5, 5, 9) is False
    assert is_safe(grid, 4, 5, 9) is False
    assert is_safe(grid, 3, 3, 1) is True


def test_is_safe_bottom_right_subgrid():
    grid = [[0 for _ in range(9)] for _ in range(9)]
    grid[8][8] = 3
    assert is_safe(grid, 6, 6, 3) is False
    assert is_safe(grid, 7, 7, 3) is False
    assert is_safe(grid, 6, 6, 5) is True


def test_is_safe_multiple_constraints():
    grid = [[0 for _ in range(9)] for _ in range(9)]
    grid[0][5] = 2
    grid[5][0] = 3
    grid[1][1] = 4
    assert is_safe(grid, 0, 0, 2) is False
    assert is_safe(grid, 0, 0, 3) is False
    assert is_safe(grid, 0, 0, 4) is False
    assert is_safe(grid, 0, 0, 1) is True


def test_is_safe_partially_filled_grid():
    grid = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    assert is_safe(grid, 0, 2, 5) is False
    assert is_safe(grid, 0, 2, 3) is False
    assert is_safe(grid, 0, 2, 1) is False
    assert is_safe(grid, 0, 2, 4) is True


def test_is_safe_all_positions():
    grid = [[0 for _ in range(9)] for _ in range(9)]
    grid[0][0] = 1
    for row in range(9):
        for col in range(9):
            if row == 0 or col == 0 or (row < 3 and col < 3):
                assert is_safe(grid, row, col, 1) is False
            else:
                assert is_safe(grid, row, col, 1) is True


def test_is_safe_boundary_values():
    grid = [[0 for _ in range(9)] for _ in range(9)]
    assert is_safe(grid, 0, 0, 1) is True
    assert is_safe(grid, 0, 0, 9) is True
    assert is_safe(grid, 8, 8, 1) is True
    assert is_safe(grid, 8, 8, 9) is True