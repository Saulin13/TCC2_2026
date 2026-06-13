import pytest
import numpy as np
from unittest.mock import patch
from graphs.multi_heuristic_astar import do_something


def test_do_something_simple_path():
    back_pointer = {
        (1, 1): (0, 0),
        (2, 2): (1, 1)
    }
    goal = (2, 2)
    start = (0, 0)
    
    with patch('graphs.multi_heuristic_astar.n', 3):
        with patch('graphs.multi_heuristic_astar.blocks', set()):
            with patch('builtins.print'):
                with pytest.raises(SystemExit):
                    do_something(back_pointer, goal, start)


def test_do_something_with_obstacles():
    back_pointer = {
        (1, 0): (0, 0),
        (2, 0): (1, 0),
        (2, 1): (2, 0),
        (2, 2): (2, 1)
    }
    goal = (2, 2)
    start = (0, 0)
    
    with patch('graphs.multi_heuristic_astar.n', 3):
        with patch('graphs.multi_heuristic_astar.blocks', {(1, 1), (1, 2)}):
            with patch('builtins.print'):
                with pytest.raises(SystemExit):
                    do_something(back_pointer, goal, start)


def test_do_something_direct_path():
    back_pointer = {
        (1, 1): (0, 0)
    }
    goal = (1, 1)
    start = (0, 0)
    
    with patch('graphs.multi_heuristic_astar.n', 2):
        with patch('graphs.multi_heuristic_astar.blocks', set()):
            with patch('builtins.print'):
                with pytest.raises(SystemExit):
                    do_something(back_pointer, goal, start)


def test_do_something_longer_path():
    back_pointer = {
        (1, 0): (0, 0),
        (2, 0): (1, 0),
        (3, 0): (2, 0),
        (3, 1): (3, 0),
        (3, 2): (3, 1),
        (3, 3): (3, 2)
    }
    goal = (3, 3)
    start = (0, 0)
    
    with patch('graphs.multi_heuristic_astar.n', 4):
        with patch('graphs.multi_heuristic_astar.blocks', set()):
            with patch('builtins.print'):
                with pytest.raises(SystemExit):
                    do_something(back_pointer, goal, start)


def test_do_something_with_multiple_obstacles():
    back_pointer = {
        (0, 1): (0, 0),
        (0, 2): (0, 1),
        (1, 2): (0, 2),
        (2, 2): (1, 2)
    }
    goal = (2, 2)
    start = (0, 0)
    
    with patch('graphs.multi_heuristic_astar.n', 3):
        with patch('graphs.multi_heuristic_astar.blocks', {(1, 0), (1, 1), (2, 1)}):
            with patch('builtins.print'):
                with pytest.raises(SystemExit):
                    do_something(back_pointer, goal, start)


def test_do_something_single_step():
    back_pointer = {
        (0, 1): (0, 0)
    }
    goal = (0, 1)
    start = (0, 0)
    
    with patch('graphs.multi_heuristic_astar.n', 2):
        with patch('graphs.multi_heuristic_astar.blocks', set()):
            with patch('builtins.print'):
                with pytest.raises(SystemExit):
                    do_something(back_pointer, goal, start)


def test_do_something_larger_grid():
    back_pointer = {
        (1, 0): (0, 0),
        (2, 0): (1, 0),
        (3, 0): (2, 0),
        (4, 0): (3, 0),
        (4, 1): (4, 0),
        (4, 2): (4, 1),
        (4, 3): (4, 2),
        (4, 4): (4, 3)
    }
    goal = (4, 4)
    start = (0, 0)
    
    with patch('graphs.multi_heuristic_astar.n', 5):
        with patch('graphs.multi_heuristic_astar.blocks', set()):
            with patch('builtins.print'):
                with pytest.raises(SystemExit):
                    do_something(back_pointer, goal, start)