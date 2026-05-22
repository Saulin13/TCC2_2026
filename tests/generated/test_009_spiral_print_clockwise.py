import pytest
from matrix.spiral_print import spiral_print_clockwise

def test_spiral_print_clockwise_normal_case(capfd):
    matrix = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12]
    ]
    spiral_print_clockwise(matrix)
    captured = capfd.readouterr()
    expected_output = "1\n2\n3\n4\n8\n12\n11\n10\n9\n5\n6\n7\n"
    assert captured.out == expected_output

def test_spiral_print_clockwise_single_row(capfd):
    matrix = [[1, 2, 3, 4]]
    spiral_print_clockwise(matrix)
    captured = capfd.readouterr()
    expected_output = "1\n2\n3\n4\n"
    assert captured.out == expected_output

def test_spiral_print_clockwise_single_column(capfd):
    matrix = [[1], [2], [3], [4]]
    spiral_print_clockwise(matrix)
    captured = capfd.readouterr()
    expected_output = "1\n2\n3\n4\n"
    assert captured.out == expected_output

def test_spiral_print_clockwise_single_element(capfd):
    matrix = [[1]]
    spiral_print_clockwise(matrix)
    captured = capfd.readouterr()
    expected_output = "1\n"
    assert captured.out == expected_output

def test_spiral_print_clockwise_empty_matrix(capfd):
    matrix = []
    spiral_print_clockwise(matrix)
    captured = capfd.readouterr()
    expected_output = "Not a valid matrix\n"
    assert captured.out == expected_output

def test_spiral_print_clockwise_non_rectangular_matrix(capfd):
    matrix = [[1, 2, 3], [4, 5], [6, 7, 8]]
    spiral_print_clockwise(matrix)
    captured = capfd.readouterr()
    expected_output = "Not a valid matrix\n"
    assert captured.out == expected_output

def test_spiral_print_clockwise_invalid_input(capfd):
    matrix = "not a matrix"
    spiral_print_clockwise(matrix)
    captured = capfd.readouterr()
    expected_output = "Not a valid matrix\n"
    assert captured.out == expected_output