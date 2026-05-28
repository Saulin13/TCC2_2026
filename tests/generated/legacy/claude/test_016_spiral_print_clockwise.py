import pytest
from io import StringIO
from unittest.mock import patch
from matrix.spiral_print import spiral_print_clockwise


def test_spiral_print_3x4_matrix():
    matrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
    expected_output = "1\n2\n3\n4\n8\n12\n11\n10\n9\n5\n6\n7\n"
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        spiral_print_clockwise(matrix)
        assert fake_out.getvalue() == expected_output


def test_spiral_print_1x1_matrix():
    matrix = [[5]]
    expected_output = "5\n"
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        spiral_print_clockwise(matrix)
        assert fake_out.getvalue() == expected_output


def test_spiral_print_2x2_matrix():
    matrix = [[1, 2], [3, 4]]
    expected_output = "1\n2\n4\n3\n"
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        spiral_print_clockwise(matrix)
        assert fake_out.getvalue() == expected_output


def test_spiral_print_1xn_matrix():
    matrix = [[1, 2, 3, 4, 5]]
    expected_output = "1\n2\n3\n4\n5\n"
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        spiral_print_clockwise(matrix)
        assert fake_out.getvalue() == expected_output


def test_spiral_print_nx1_matrix():
    matrix = [[1], [2], [3], [4]]
    expected_output = "1\n2\n3\n4\n"
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        spiral_print_clockwise(matrix)
        assert fake_out.getvalue() == expected_output


def test_spiral_print_3x3_matrix():
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    expected_output = "1\n2\n3\n6\n9\n8\n7\n4\n5\n"
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        spiral_print_clockwise(matrix)
        assert fake_out.getvalue() == expected_output


def test_spiral_print_4x4_matrix():
    matrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
    expected_output = "1\n2\n3\n4\n8\n12\n16\n15\n14\n13\n9\n5\n6\n7\n11\n10\n"
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        spiral_print_clockwise(matrix)
        assert fake_out.getvalue() == expected_output


def test_spiral_print_empty_matrix():
    matrix = []
    expected_output = "Not a valid matrix\n"
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        spiral_print_clockwise(matrix)
        assert fake_out.getvalue() == expected_output


def test_spiral_print_invalid_matrix_jagged():
    matrix = [[1, 2, 3], [4, 5]]
    expected_output = "Not a valid matrix\n"
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        spiral_print_clockwise(matrix)
        assert fake_out.getvalue() == expected_output


def test_spiral_print_2x3_matrix():
    matrix = [[1, 2, 3], [4, 5, 6]]
    expected_output = "1\n2\n3\n6\n5\n4\n"
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        spiral_print_clockwise(matrix)
        assert fake_out.getvalue() == expected_output


def test_spiral_print_3x2_matrix():
    matrix = [[1, 2], [3, 4], [5, 6]]
    expected_output = "1\n2\n4\n6\n5\n3\n"
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        spiral_print_clockwise(matrix)
        assert fake_out.getvalue() == expected_output


def test_spiral_print_with_negative_numbers():
    matrix = [[-1, -2, -3], [-4, -5, -6]]
    expected_output = "-1\n-2\n-3\n-6\n-5\n-4\n"
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        spiral_print_clockwise(matrix)
        assert fake_out.getvalue() == expected_output


def test_spiral_print_with_zeros():
    matrix = [[0, 0], [0, 0]]
    expected_output = "0\n0\n0\n0\n"
    
    with patch('sys.stdout', new=StringIO()) as fake_out:
        spiral_print_clockwise(matrix)
        assert fake_out.getvalue() == expected_output