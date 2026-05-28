import pytest
import sys
from io import StringIO
from unittest.mock import patch
import numpy as np
from graphs.multi_heuristic_astar import do_something


def test_do_something_simple_path():
    """Test with a simple path from start to goal."""
    with patch('graphs.multi_heuristic_astar.n', 3):
        with patch('graphs.multi_heuristic_astar.blocks', set()):
            back_pointer = {
                (2, 2): (1, 2),
                (1, 2): (0, 2),
                (0, 2): (0, 1),
                (0, 1): (0, 0)
            }
            goal = (2, 2)
            start = (0, 0)
            
            captured_output = StringIO()
            with patch('sys.stdout', captured_output):
                with pytest.raises(SystemExit):
                    do_something(back_pointer, goal, start)
            
            output = captured_output.getvalue()
            assert "- is the path taken by algorithm" in output
            assert "# is an obstacle" in output
            assert "PATH TAKEN BY THE ALGORITHM IS:-" in output
            assert "(2, 2)" in output or "2, 2" in output


def test_do_something_with_obstacles():
    """Test with obstacles in the grid."""
    with patch('graphs.multi_heuristic_astar.n', 4):
        with patch('graphs.multi_heuristic_astar.blocks', {(1, 1), (2, 1)}):
            back_pointer = {
                (3, 3): (2, 3),
                (2, 3): (1, 3),
                (1, 3): (0, 3),
                (0, 3): (0, 2),
                (0, 2): (0, 1),
                (0, 1): (0, 0)
            }
            goal = (3, 3)
            start = (0, 0)
            
            captured_output = StringIO()
            with patch('sys.stdout', captured_output):
                with pytest.raises(SystemExit):
                    do_something(back_pointer, goal, start)
            
            output = captured_output.getvalue()
            assert "#" in output
            assert "-" in output
            assert "Start position" in output
            assert "End position" in output


def test_do_something_direct_path():
    """Test with a direct diagonal-like path."""
    with patch('graphs.multi_heuristic_astar.n', 5):
        with patch('graphs.multi_heuristic_astar.blocks', set()):
            back_pointer = {
                (4, 4): (3, 3),
                (3, 3): (2, 2),
                (2, 2): (1, 1),
                (1, 1): (0, 0)
            }
            goal = (4, 4)
            start = (0, 0)
            
            captured_output = StringIO()
            with patch('sys.stdout', captured_output):
                with pytest.raises(SystemExit):
                    do_something(back_pointer, goal, start)
            
            output = captured_output.getvalue()
            assert "(4, 4)" in output or "4, 4" in output
            assert "(3, 3)" in output or "3, 3" in output
            assert "(2, 2)" in output or "2, 2" in output
            assert "(1, 1)" in output or "1, 1" in output


def test_do_something_single_step():
    """Test with minimal path (single step)."""
    with patch('graphs.multi_heuristic_astar.n', 2):
        with patch('graphs.multi_heuristic_astar.blocks', set()):
            back_pointer = {
                (1, 1): (0, 0)
            }
            goal = (1, 1)
            start = (0, 0)
            
            captured_output = StringIO()
            with patch('sys.stdout', captured_output):
                with pytest.raises(SystemExit):
                    do_something(back_pointer, goal, start)
            
            output = captured_output.getvalue()
            assert "(1, 1)" in output or "1, 1" in output
            assert "(0, 0)" in output or "0, 0" in output


def test_do_something_exits_with_sys_exit():
    """Test that function calls sys.exit() as expected."""
    with patch('graphs.multi_heuristic_astar.n', 2):
        with patch('graphs.multi_heuristic_astar.blocks', set()):
            back_pointer = {
                (1, 1): (0, 0)
            }
            goal = (1, 1)
            start = (0, 0)
            
            with patch('sys.stdout', StringIO()):
                with pytest.raises(SystemExit) as exc_info:
                    do_something(back_pointer, goal, start)
                
                assert exc_info.type == SystemExit