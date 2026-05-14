import pytest
from io import StringIO
from contextlib import redirect_stdout
from other.activity_selection import print_max_activities

def test_print_max_activities_normal_case():
    start = [1, 3, 0, 5, 8, 5]
    finish = [2, 4, 6, 7, 9, 9]
    expected_output = "The following activities are selected:\n0,1,3,4,\n"
    f = StringIO()
    with redirect_stdout(f):
        print_max_activities(start, finish)
    assert f.getvalue() == expected_output

def test_print_max_activities_edge_case_empty():
    start = []
    finish = []
    expected_output = "The following activities are selected:\n"
    f = StringIO()
    with redirect_stdout(f):
        print_max_activities(start, finish)
    assert f.getvalue() == expected_output

def test_print_max_activities_edge_case_single_activity():
    start = [1]
    finish = [2]
    expected_output = "The following activities are selected:\n0,\n"
    f = StringIO()
    with redirect_stdout(f):
        print_max_activities(start, finish)
    assert f.getvalue() == expected_output

def test_print_max_activities_no_activities_selected():
    start = [5, 6, 7]
    finish = [8, 9, 10]
    expected_output = "The following activities are selected:\n0,\n"
    f = StringIO()
    with redirect_stdout(f):
        print_max_activities(start, finish)
    assert f.getvalue() == expected_output

def test_print_max_activities_invalid_input():
    start = [1, 3, 0]
    finish = [2, 4]  # Mismatched lengths
    with pytest.raises(IndexError):
        print_max_activities(start, finish)