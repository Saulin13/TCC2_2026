import pytest
from machine_learning.frequent_pattern_growth import create_tree


def test_create_tree_basic():
    data_set = [
        ['A', 'B', 'C'],
        ['A', 'C'],
        ['A', 'B', 'E'],
        ['A', 'B', 'C', 'E'],
        ['B', 'E']
    ]
    min_sup = 2
    fp_tree, header_table = create_tree(data_set, min_sup)
    
    assert fp_tree.name == 'Null Set'
    assert fp_tree.count == 1
    assert fp_tree.parent is None
    assert len(header_table) == 4
    assert 'A' in header_table
    assert 'B' in header_table
    assert 'C' in header_table
    assert 'E' in header_table
    assert header_table['A'][0] == 4


def test_create_tree_single_transaction():
    data_set = [['A', 'B', 'C']]
    min_sup = 1
    fp_tree, header_table = create_tree(data_set, min_sup)
    
    assert fp_tree.name == 'Null Set'
    assert len(header_table) == 3
    assert 'A' in header_table
    assert 'B' in header_table
    assert 'C' in header_table


def test_create_tree_empty_dataset():
    data_set = []
    min_sup = 1
    fp_tree, header_table = create_tree(data_set, min_sup)
    
    assert fp_tree.name == 'Null Set'
    assert len(header_table) == 0
    assert header_table == {}


def test_create_tree_empty_transactions():
    data_set = [[], [], []]
    min_sup = 1
    fp_tree, header_table = create_tree(data_set, min_sup)
    
    assert fp_tree.name == 'Null Set'
    assert len(header_table) == 0
    assert header_table == {}


def test_create_tree_high_min_sup_prunes_all():
    data_set = [
        ['A', 'B'],
        ['C', 'D'],
        ['E', 'F']
    ]
    min_sup = 5
    fp_tree, header_table = create_tree(data_set, min_sup)
    
    assert fp_tree.name == 'Null Set'
    assert len(header_table) == 0
    assert header_table == {}


def test_create_tree_min_sup_default():
    data_set = [
        ['A'],
        ['B'],
        ['C']
    ]
    fp_tree, header_table = create_tree(data_set)
    
    assert fp_tree.name == 'Null Set'
    assert len(header_table) == 3
    assert 'A' in header_table
    assert 'B' in header_table
    assert 'C' in header_table


def test_create_tree_identical_transactions():
    data_set = [
        ['A', 'B', 'C'],
        ['A', 'B', 'C'],
        ['A', 'B', 'C']
    ]
    min_sup = 2
    fp_tree, header_table = create_tree(data_set, min_sup)
    
    assert fp_tree.name == 'Null Set'
    assert len(header_table) == 3
    assert header_table['A'][0] == 3
    assert header_table['B'][0] == 3
    assert header_table['C'][0] == 3


def test_create_tree_partial_pruning():
    data_set = [
        ['A', 'B', 'C'],
        ['A', 'B'],
        ['A', 'D']
    ]
    min_sup = 2
    fp_tree, header_table = create_tree(data_set, min_sup)
    
    assert len(header_table) == 2
    assert 'A' in header_table
    assert 'B' in header_table
    assert 'C' not in header_table
    assert 'D' not in header_table
    assert header_table['A'][0] == 3
    assert header_table['B'][0] == 2


def test_create_tree_single_item_transactions():
    data_set = [
        ['A'],
        ['A'],
        ['B'],
        ['B'],
        ['B']
    ]
    min_sup = 2
    fp_tree, header_table = create_tree(data_set, min_sup)
    
    assert fp_tree.name == 'Null Set'
    assert len(header_table) == 2
    assert header_table['A'][0] == 2
    assert header_table['B'][0] == 3


def test_create_tree_numeric_items():
    data_set = [
        [1, 2, 3],
        [1, 2],
        [1, 3],
        [2, 3]
    ]
    min_sup = 2
    fp_tree, header_table = create_tree(data_set, min_sup)
    
    assert fp_tree.name == 'Null Set'
    assert len(header_table) == 3
    assert 1 in header_table
    assert 2 in header_table
    assert 3 in header_table


def test_create_tree_mixed_length_transactions():
    data_set = [
        ['A'],
        ['A', 'B'],
        ['A', 'B', 'C'],
        ['A', 'B', 'C', 'D']
    ]
    min_sup = 2
    fp_tree, header_table = create_tree(data_set, min_sup)
    
    assert fp_tree.name == 'Null Set'
    assert len(header_table) == 3
    assert header_table['A'][0] == 4
    assert header_table['B'][0] == 3
    assert header_table['C'][0] == 2