import pytest
from io import StringIO
import sys
from matrix.spiral_print import spiral_print_clockwise


def capture_print_output(func, *args, **kwargs):
    """Helper function to capture print output"""
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    try:
        func(*args, **kwargs)
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout
    return output


def test_spiral_print_3x4_matrix(capsys):
    """Test with a 3x4 matrix"""
    matrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
    spiral_print_clockwise(matrix)
    captured = capsys.readouterr()
    expected = "1\n2\n3\n4\n8\n12\n11\n10\n9\n5\n6\n7\n"
    assert captured.out == expected


def test_spiral_print_1x1_matrix(capsys):
    """Test with a single element matrix"""
    matrix = [[5]]
    spiral_print_clockwise(matrix)
    captured = capsys.readouterr()
    expected = "5\n"
    assert captured.out == expected


def test_spiral_print_2x2_matrix(capsys):
    """Test with a 2x2 matrix"""
    matrix = [[1, 2], [3, 4]]
    spiral_print_clockwise(matrix)
    captured = capsys.readouterr()
    expected = "1\n2\n4\n3\n"
    assert captured.out == expected


def test_spiral_print_1xn_matrix(capsys):
    """Test with a single row matrix"""
    matrix = [[1, 2, 3, 4, 5]]
    spiral_print_clockwise(matrix)
    captured = capsys.readouterr()
    expected = "1\n2\n3\n4\n5\n"
    assert captured.out == expected


def test_spiral_print_nx1_matrix(capsys):
    """Test with a single column matrix"""
    matrix = [[1], [2], [3], [4]]
    spiral_print_clockwise(matrix)
    captured = capsys.readouterr()
    expected = "1\n2\n3\n4\n"
    assert captured.out == expected


def test_spiral_print_4x4_matrix(capsys):
    """Test with a 4x4 square matrix"""
    matrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
    spiral_print_clockwise(matrix)
    captured = capsys.readouterr()
    expected = "1\n2\n3\n4\n8\n12\n16\n15\n14\n13\n9\n5\n6\n7\n11\n10\n"
    assert captured.out == expected


def test_spiral_print_5x3_matrix(capsys):
    """Test with a 5x3 matrix (more rows than columns)"""
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15]]
    spiral_print_clockwise(matrix)
    captured = capsys.readouterr()
    expected = "1\n2\n3\n6\n9\n12\n15\n14\n13\n10\n7\n4\n5\n8\n11\n"
    assert captured.out == expected


def test_spiral_print_empty_matrix(capsys):
    """Test with an empty matrix"""
    matrix = []
    spiral_print_clockwise(matrix)
    captured = capsys.readouterr()
    assert captured.out == ""


def test_spiral_print_invalid_matrix_jagged(capsys):
    """Test with an invalid jagged matrix (different row lengths)"""
    matrix = [[1, 2, 3], [4, 5], [6, 7, 8]]
    spiral_print_clockwise(matrix)
    captured = capsys.readouterr()
    assert "Not a valid matrix" in captured.out


def test_spiral_print_2x3_matrix(capsys):
    """Test with a 2x3 matrix"""
    matrix = [[1, 2, 3], [4, 5, 6]]
    spiral_print_clockwise(matrix)
    captured = capsys.readouterr()
    expected = "1\n2\n3\n6\n5\n4\n"
    assert captured.out == expected


def test_spiral_print_3x2_matrix(capsys):
    """Test with a 3x2 matrix"""
    matrix = [[1, 2], [3, 4], [5, 6]]
    spiral_print_clockwise(matrix)
    captured = capsys.readouterr()
    expected = "1\n2\n4\n6\n5\n3\n"
    assert captured.out == expected


def test_spiral_print_with_negative_numbers(capsys):
    """Test with negative numbers"""
    matrix = [[-1, -2, -3], [-4, -5, -6]]
    spiral_print_clockwise(matrix)
    captured = capsys.readouterr()
    expected = "-1\n-2\n-3\n-6\n-5\n-4\n"
    assert captured.out == expected


def test_spiral_print_with_zeros(capsys):
    """Test with zeros"""
    matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    spiral_print_clockwise(matrix)
    captured = capsys.readouterr()
    expected = "0\n0\n0\n0\n0\n0\n0\n0\n0\n"
    assert captured.out == expected