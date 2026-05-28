import pytest
from machine_learning.frequent_pattern_growth import create_tree
from machine_learning.frequent_pattern_growth import TreeNode

def test_create_tree_normal_case():
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
    assert len(header_table) == 4
    assert sorted(header_table) == ['A', 'B', 'C', 'E']
    assert header_table["A"][0] == [4, None]
    assert header_table["E"][1].name == 'E'
    assert sorted(fp_tree.children) == ['A', 'B']
    assert fp_tree.children['A'].name == 'A'
    assert sorted(fp_tree.children['A'].children) == ['B', 'C']

def test_create_tree_edge_case_empty_dataset():
    data_set = []
    min_sup = 1
    fp_tree, header_table = create_tree(data_set, min_sup)

    assert fp_tree.name == 'Null Set'
    assert len(header_table) == 0

def test_create_tree_edge_case_high_min_sup():
    data_set = [
        ['A', 'B', 'C'],
        ['A', 'C'],
        ['A', 'B', 'E'],
        ['A', 'B', 'C', 'E'],
        ['B', 'E']
    ]
    min_sup = 10
    fp_tree, header_table = create_tree(data_set, min_sup)

    assert fp_tree.name == 'Null Set'
    assert len(header_table) == 0

def test_create_tree_exception_invalid_min_sup():
    data_set = [
        ['A', 'B', 'C'],
        ['A', 'C'],
        ['A', 'B', 'E'],
        ['A', 'B', 'C', 'E'],
        ['B', 'E']
    ]
    min_sup = -1
    with pytest.raises(ValueError):
        create_tree(data_set, min_sup)
```

Note: The test `test_create_tree_exception_invalid_min_sup` assumes that the `create_tree` function should raise a `ValueError` when `min_sup` is negative. If the original function does not raise an exception for this case, you may need to adjust the test or the function accordingly.