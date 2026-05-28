import pytest
from graphs.multi_heuristic_astar import do_something
import numpy as np
import sys

def test_do_something_normal_case(monkeypatch):
    # Mock sys.exit to prevent the test from exiting
    monkeypatch.setattr(sys, "exit", lambda: None)
    
    n = 5
    blocks = {(1, 3), (2, 2), (3, 1)}
    back_pointer = {
        (4, 4): (3, 4),
        (3, 4): (2, 4),
        (2, 4): (1, 4),
        (1, 4): (0, 4),
        (0, 4): (0, 3),
        (0, 3): (0, 2),
        (0, 2): (0, 1),
        (0, 1): (0, 0)
    }
    goal = (4, 4)
    start = (0, 0)

    expected_output = [
        "- - - - <-- End position ",
        "* * * * * ",
        "* * # * * ",
        "* # * * * ",
        "- - - - - ",
        "^",
        "Start position",
        "",
        "# is an obstacle",
        "- is the path taken by algorithm",
        "PATH TAKEN BY THE ALGORITHM IS:-",
        "(4, 4) (3, 4) (2, 4) (1, 4) (0, 4) (0, 3) (0, 2) (0, 1) (0, 0)"
    ]

    # Capture the output
    output = []
    def mock_print(*args, **kwargs):
        output.append(" ".join(map(str, args)))

    monkeypatch.setattr("builtins.print", mock_print)

    # Run the function
    do_something(back_pointer, goal, start)

    # Assert the output
    assert output == expected_output

def test_do_something_edge_case_no_path(monkeypatch):
    # Mock sys.exit to prevent the test from exiting
    monkeypatch.setattr(sys, "exit", lambda: None)
    
    n = 5
    blocks = {(1, 3), (2, 2), (3, 1)}
    back_pointer = {
        (4, 4): (3, 4),
        (3, 4): (2, 4),
        (2, 4): (1, 4),
        (1, 4): (0, 4),
        (0, 4): (0, 3),
        (0, 3): (0, 2),
        (0, 2): (0, 1),
        (0, 1): (0, 0)
    }
    goal = (4, 4)
    start = (4, 4)  # Start is the same as goal

    expected_output = [
        "* * * * <-- End position ",
        "* * * * * ",
        "* * # * * ",
        "* # * * * ",
        "* * * * - ",
        "^",
        "Start position",
        "",
        "# is an obstacle",
        "- is the path taken by algorithm",
        "PATH TAKEN BY THE ALGORITHM IS:-",
        "(4, 4)"
    ]

    # Capture the output
    output = []
    def mock_print(*args, **kwargs):
        output.append(" ".join(map(str, args)))

    monkeypatch.setattr("builtins.print", mock_print)

    # Run the function
    do_something(back_pointer, goal, start)

    # Assert the output
    assert output == expected_output

def test_do_something_exception_case(monkeypatch):
    # Mock sys.exit to prevent the test from exiting
    monkeypatch.setattr(sys, "exit", lambda: None)
    
    n = 5
    blocks = {(1, 3), (2, 2), (3, 1)}
    back_pointer = {
        (4, 4): (3, 4),
        (3, 4): (2, 4),
        (2, 4): (1, 4),
        (1, 4): (0, 4),
        (0, 4): (0, 3),
        (0, 3): (0, 2),
        (0, 2): (0, 1),
        (0, 1): (0, 0)
    }
    goal = (4, 4)
    start = (5, 5)  # Invalid start position

    # Capture the output
    output = []
    def mock_print(*args, **kwargs):
        output.append(" ".join(map(str, args)))

    monkeypatch.setattr("builtins.print", mock_print)

    # Run the function
    with pytest.raises(KeyError):
        do_something(back_pointer, goal, start)