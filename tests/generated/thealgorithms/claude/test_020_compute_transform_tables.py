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
    costs, operations = compute_transform_tables("abc", "", 1, 2, 5, 4)
    assert costs == [[0], [5], [10], [15]]
    assert operations == [['0'], ['Da'], ['Db'], ['Dc']]


def test_identical_strings():
    costs, operations = compute_transform_tables("hello", "hello", 1, 10, 10, 10)
    assert costs[0][0] == 0
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
    costs, operations = compute_transform_tables("a", "b", 1, 5, 10, 10)
    assert costs == [[0, 10], [10, 5]]
    assert operations == [['0', 'Ib'], ['Da', 'Rab']]


def test_single_character_delete():
    costs, operations = compute_transform_tables("a", "", 1, 10, 3, 10)
    assert costs == [[0], [3]]
    assert operations == [['0'], ['Da']]


def test_single_character_insert():
    costs, operations = compute_transform_tables("", "a", 1, 10, 10, 2)
    assert costs == [[0, 2]]
    assert operations == [['0', 'Ia']]


def test_longer_strings():
    costs, operations = compute_transform_tables("kitten", "sitting", 0, 1, 1, 1)
    assert len(costs) == 7
    assert len(costs[0]) == 8
    assert costs[0][0] == 0
    assert costs[6][7] == 3


def test_all_operations_used():
    costs, operations = compute_transform_tables("abc", "def", 1, 2, 3, 4)
    assert len(costs) == 4
    assert len(costs[0]) == 4
    assert costs[0][0] == 0


def test_zero_costs():
    costs, operations = compute_transform_tables("ab", "ab", 0, 0, 0, 0)
    assert costs[0][0] == 0
    assert costs[2][2] == 0
    assert operations[1][1] == 'Ca'
    assert operations[2][2] == 'Cb'


def test_high_copy_cost_favors_replace():
    costs, operations = compute_transform_tables("a", "a", 100, 1, 10, 10)
    assert costs[1][1] == 1
    assert operations[1][1] == 'Raa'


def test_low_delete_cost():
    costs, operations = compute_transform_tables("abc", "a", 1, 10, 1, 10)
    assert costs[3][1] == 3
    assert operations[3][1] == 'Dc'


def test_low_insert_cost():
    costs, operations = compute_transform_tables("a", "abc", 1, 10, 10, 1)
    assert costs[1][3] == 3
    assert operations[1][3] == 'Ic'


def test_multiple_same_characters():
    costs, operations = compute_transform_tables("aaa", "aaa", 1, 10, 10, 10)
    assert costs[3][3] == 3
    assert operations[1][1] == 'Ca'
    assert operations[2][2] == 'Ca'
    assert operations[3][3] == 'Ca'


def test_reverse_strings():
    costs, operations = compute_transform_tables("abc", "cba", 1, 2, 3, 3)
    assert len(costs) == 4
    assert len(costs[0]) == 4
    assert costs[0][0] == 0


def test_special_characters():
    costs, operations = compute_transform_tables("a!b", "a@b", 1, 2, 3, 3)
    assert len(costs) == 4
    assert len(costs[0]) == 4
    assert operations[2][2] == 'R!@'


def test_numeric_strings():
    costs, operations = compute_transform_tables("123", "456", 1, 2, 3, 3)
    assert len(costs) == 4
    assert len(costs[0]) == 4
    assert operations[1][1] == 'R14'