import pytest
from data_structures.binary_tree.binary_tree_traversals import get_nodes_from_right_to_left
from data_structures.binary_tree.node import Node

def make_tree():
    # Helper function to create a sample binary tree
    #        1
    #       / \
    #      2   3
    #     / \   \
    #    4   5   6
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)
    root.right.right = Node(6)
    return root

def test_get_nodes_from_right_to_left_normal_case():
    tree = make_tree()
    assert list(get_nodes_from_right_to_left(tree, 1)) == [1]
    assert list(get_nodes_from_right_to_left(tree, 2)) == [3, 2]
    assert list(get_nodes_from_right_to_left(tree, 3)) == [6, 5, 4]

def test_get_nodes_from_right_to_left_edge_case_empty_tree():
    assert list(get_nodes_from_right_to_left(None, 1)) == []

def test_get_nodes_from_right_to_left_edge_case_single_node():
    root = Node(10)
    assert list(get_nodes_from_right_to_left(root, 1)) == [10]
    assert list(get_nodes_from_right_to_left(root, 2)) == []

def test_get_nodes_from_right_to_left_edge_case_level_greater_than_tree_height():
    tree = make_tree()
    assert list(get_nodes_from_right_to_left(tree, 4)) == []

def test_get_nodes_from_right_to_left_failure_invalid_level():
    tree = make_tree()
    with pytest.raises(ValueError):
        list(get_nodes_from_right_to_left(tree, 0))
```

Note: The `Node` class and its implementation are assumed to be available in the `data_structures.binary_tree.node` module. The `make_tree` function is a helper to create a sample binary tree for testing purposes.