import pytest
from strings.min_cost_string_conversion import compute_transform_tables


def test_empty_strings():
    costs, operations = compute_transform_tables("", "", 1, 2, 3, 3)
    assert costs == [[0]]
    assert operations == [['0']]


def test_empty_source_string():
    costs, operations = compute_transform_tables("", "abc", 1, 2, 3, 4)
    assert costs == [[0, 4, 8, 12]]
    assert operations == [['0', 'Ia', 'Ib', 'Ic']]


def test_empty_destination_string():
    costs, operations = compute_transform_tables("abc", "", 1, 2, 3, 4)
    assert costs == [[0], [3], [6], [9]]
    assert operations == [['0'], ['Da'], ['Db'], ['Dc']]


def test_identical_strings():
    costs, operations = compute_transform_tables("hello", "hello", 1, 5, 5, 5)
    assert costs[5][5] == 5
    assert operations[1][1] == 'Ch'
    assert operations[2][2] == 'Ce'
    assert operations[5][5] == 'Co'


def test_cat_to_cut():
    costs, operations = compute_transform_tables("cat", "cut", 1, 2, 3, 3)
    assert costs[0][:4] == [0, 3, 6, 9]
    assert costs[2][:4] == [6, 4, 3, 6]
    assert operations[0][:4] == ['0', 'Ic', 'Iu', 'It']
    assert operations[3][:4] == ['Dt', 'Dt', 'Rtu', 'Ct']


def test_single_character_copy():
    costs, operations = compute_transform_tables("a", "a", 1, 10, 10, 10)
    assert costs == [[0, 10], [10, 1]]
    assert operations == [['0', 'Ia'], ['Da', 'Ca']]


def test_single_character_replace():
    costs, operations = compute_transform_tables("a", "b", 1, 2, 3, 3)
    assert costs == [[0, 3], [3, 2]]
    assert operations == [['0', 'Ib'], ['Da', 'Rab']]


def test_delete_cheaper_than_replace():
    costs, operations = compute_transform_tables("ab", "a", 1, 10, 2, 10)
    assert costs[2][1] == 2
    assert operations[2][1] == 'Db'


def test_insert_cheaper_than_replace():
    costs, operations = compute_transform_tables("a", "ab", 1, 10, 10, 2)
    assert costs[1][2] == 2
    assert operations[1][2] == 'Ib'


def test_longer_strings():
    costs, operations = compute_transform_tables("kitten", "sitting", 1, 2, 3, 3)
    assert len(costs) == 7
    assert len(costs[0]) == 8
    assert len(operations) == 7
    assert len(operations[0]) == 8
    assert costs[0][0] == 0
    assert operations[0][0] == '0'


def test_all_operations_used():
    costs, operations = compute_transform_tables("abc", "xyz", 1, 2, 3, 3)
    assert costs[3][3] == 6
    assert 'Rax' in operations[1][1] or 'Ixy' in str(operations) or 'Da' in str(operations)


def test_zero_costs():
    costs, operations = compute_transform_tables("ab", "ab", 0, 0, 0, 0)
    assert costs[2][2] == 0
    assert operations[1][1] == 'Ca'
    assert operations[2][2] == 'Cb'


def test_high_copy_cost():
    costs, operations = compute_transform_tables("aa", "aa", 100, 1, 1, 1)
    assert costs[1][1] == 1
    assert operations[1][1] == 'Raa'


def test_different_length_strings():
    costs, operations = compute_transform_tables("short", "verylongstring", 1, 2, 3, 3)
    assert len(costs) == 6
    assert len(costs[0]) == 15
    assert costs[0][0] == 0


def test_special_characters():
    costs, operations = compute_transform_tables("a!b", "a@b", 1, 2, 3, 3)
    assert operations[2][2] == 'R!@'
    assert costs[3][3] == 3


def test_numeric_string():
    costs, operations = compute_transform_tables("123", "456", 1, 2, 3, 3)
    assert operations[1][1] == 'R14'
    assert operations[2][2] == 'R25'
    assert operations[3][3] == 'R36'


def test_whitespace_characters():
    costs, operations = compute_transform_tables("a b", "a  b", 1, 2, 3, 3)
    assert len(costs) == 4
    assert len(costs[0]) == 5
    assert operations[2][2] == 'C '