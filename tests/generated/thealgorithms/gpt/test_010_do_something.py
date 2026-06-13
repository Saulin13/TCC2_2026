import pytest
from graphs.multi_heuristic_astar import do_something
import numpy as np

def test_do_something_normal_case(mocker):
    n = 5
    blocks = {(1, 1), (2, 2), (3, 3)}
    back_pointer = {
        (4, 4): (3, 4),
        (3, 4): (2, 4),
        (2, 4): (1, 4),
        (1, 4): (0, 4),
        (0, 4): (0, 3),
        (0, 3): (0, 2),
        (0, 2): (0, 1),
        (0, 1): (0, 0),
        (0, 0): None
    }
    goal = (4, 4)
    start = (0, 0)

    mocker.patch('builtins.print')
    mocker.patch('sys.exit')

    do_something(back_pointer, goal, start)

    expected_grid = np.array([
        ['-', '-', '-', '-', '-'],
        ['*', '*', '*', '*', '-'],
        ['*', '*', '*', '*', '-'],
        ['*', '*', '*', '*', '-'],
        ['*', '*', '*', '*', '-']
    ])
    
    # Check if the grid was printed correctly
    for i in range(n):
        for j in range(n):
            if (j, (n - 1) - i) in blocks:
                assert print.call_args_list[i * n + j][0][0] == '#'
            else:
                assert print.call_args_list[i * n + j][0][0] == expected_grid[i][j]

def test_do_something_edge_case_empty_path(mocker):
    n = 3
    blocks = set()
    back_pointer = {
        (2, 2): (1, 2),
        (1, 2): (0, 2),
        (0, 2): (0, 1),
        (0, 1): (0, 0),
        (0, 0): None
    }
    goal = (2, 2)
    start = (0, 0)

    mocker.patch('builtins.print')
    mocker.patch('sys.exit')

    do_something(back_pointer, goal, start)

    expected_grid = np.array([
        ['-', '-', '-'],
        ['*', '*', '-'],
        ['*', '*', '-']
    ])
    
    # Check if the grid was printed correctly
    for i in range(n):
        for j in range(n):
            assert print.call_args_list[i * n + j][0][0] == expected_grid[i][j]

def test_do_something_exception_case(mocker):
    n = 3
    blocks = set()
    back_pointer = {
        (2, 2): (1, 2),
        (1, 2): (0, 2),
        (0, 2): (0, 1),
        (0, 1): (0, 0)
        # Missing start point
    }
    goal = (2, 2)
    start = (0, 0)

    mocker.patch('builtins.print')
    mocker.patch('sys.exit')

    with pytest.raises(KeyError):
        do_something(back_pointer, goal, start)