import pytest
from strings.min_cost_string_conversion import compute_transform_tables

def test_compute_transform_tables_basic():
    costs, operations = compute_transform_tables("cat", "cut", 1, 2, 3, 3)
    assert costs[0][:4] == [0, 3, 6, 9]
    assert costs[2][:4] == [6, 4, 3, 6]
    assert operations[0][:4] == ['0', 'Ic', 'Iu', 'It']
    assert operations[3][:4] == ['Dt', 'Dt', 'Rtu', 'Ct']

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
    costs, operations = compute_transform_tables("abc", "def", 1, 1, 3, 3)
    assert costs == [
        [0, 3, 6, 9],
        [3, 1, 4, 7],
        [6, 4, 2, 5],
        [9, 7, 5, 3]
    ]
    assert operations == [
        ['0', 'Id', 'Ie', 'If'],
        ['Da', 'Rad', 'Rea', 'Rfa'],
        ['Db', 'Rbd', 'Reb', 'Rfb'],
        ['Dc', 'Rcd', 'Rec', 'Rfc']
    ]

def test_compute_transform_tables_copy_and_replace():
    costs, operations = compute_transform_tables("abc", "adc", 1, 2, 3, 3)
    assert costs == [
        [0, 3, 6, 9],
        [3, 1, 4, 7],
        [6, 4, 2, 5],
        [9, 7, 5, 3]
    ]
    assert operations == [
        ['0', 'Ia', 'Id', 'Ic'],
        ['Da', 'Ca', 'Id', 'Ic'],
        ['Db', 'Rd', 'Cd', 'Ic'],
        ['Dc', 'Rd', 'Re', 'Cc']
    ]

def test_compute_transform_tables_invalid_costs():
    with pytest.raises(ValueError):
        compute_transform_tables("abc", "def", -1, 2, 3, 3)