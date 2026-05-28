import pytest
from strings.min_cost_string_conversion import compute_transform_tables

def test_compute_transform_tables_normal_case():
    costs, operations = compute_transform_tables("cat", "cut", 1, 2, 3, 3)
    assert costs == [
        [0, 3, 6, 9],
        [3, 2, 5, 8],
        [6, 5, 4, 7],
        [9, 8, 6, 6]
    ]
    assert operations == [
        ['0', 'Ic', 'Iu', 'It'],
        ['Dc', 'Rc', 'Iu', 'It'],
        ['Dc', 'Dc', 'Cu', 'It'],
        ['Dc', 'Dc', 'Rtu', 'Ct']
    ]

def test_compute_transform_tables_empty_strings():
    costs, operations = compute_transform_tables("", "", 1, 2, 3, 3)
    assert costs == [[0]]
    assert operations == [['0']]

def test_compute_transform_tables_insert_only():
    costs, operations = compute_transform_tables("", "abc", 1, 2, 3, 1)
    assert costs == [[0, 1, 2, 3]]
    assert operations == [['0', 'Ia', 'Ib', 'Ic']]

def test_compute_transform_tables_delete_only():
    costs, operations = compute_transform_tables("abc", "", 1, 2, 1, 3)
    assert costs == [[0], [1], [2], [3]]
    assert operations == [['0'], ['Da'], ['Db'], ['Dc']]

def test_compute_transform_tables_replace_only():
    costs, operations = compute_transform_tables("abc", "xyz", 1, 1, 3, 3)
    assert costs == [
        [0, 3, 6, 9],
        [3, 1, 4, 7],
        [6, 4, 2, 5],
        [9, 7, 5, 3]
    ]
    assert operations == [
        ['0', 'Ix', 'Iy', 'Iz'],
        ['Da', 'Rax', 'Ix', 'Ix'],
        ['Db', 'Db', 'Rby', 'Iy'],
        ['Dc', 'Dc', 'Dc', 'Rcz']
    ]

def test_compute_transform_tables_copy_only():
    costs, operations = compute_transform_tables("abc", "abc", 0, 2, 3, 3)
    assert costs == [
        [0, 3, 6, 9],
        [3, 0, 3, 6],
        [6, 3, 0, 3],
        [9, 6, 3, 0]
    ]
    assert operations == [
        ['0', 'Ia', 'Ib', 'Ic'],
        ['Da', 'Ca', 'Ib', 'Ic'],
        ['Db', 'Db', 'Cb', 'Ic'],
        ['Dc', 'Dc', 'Dc', 'Cc']
    ]

def test_compute_transform_tables_exception_path():
    with pytest.raises(TypeError):
        compute_transform_tables(None, "abc", 1, 2, 3, 3)