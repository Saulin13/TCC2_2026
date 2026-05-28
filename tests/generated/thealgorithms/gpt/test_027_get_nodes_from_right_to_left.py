import pytest
from data_structures.binary_tree.binary_tree_traversals import get_nodes_from_right_to_left
from data_structures.binary_tree.node import Node

def make_tree():
    # Helper function to create a binary tree for testing
    # Tree structure:
    #       1
    #      / \
    #     2   3
    #    / \   \
    #   4   5   6
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)
    root.right.right = Node(6)
    return root

def test_get_nodes_from_right_to_left_normal_case():
    root = make_tree()
    assert list(get_nodes_from_right_to_left(root, 1)) == [1]
    assert list(get_nodes_from_right_to_left(root, 2)) == [3, 2]
    assert list(get_nodes_from_right_to_left(root, 3)) == [6, 5, 4]

def test_get_nodes_from_right_to_left_edge_case_empty_tree():
    root = None
    assert list(get_nodes_from_right_to_left(root, 1)) == []

def test_get_nodes_from_right_to_left_edge_case_single_node():
    root = Node(1)
    assert list(get_nodes_from_right_to_left(root, 1)) == [1]
    assert list(get_nodes_from_right_to_left(root, 2)) == []

def test_get_nodes_from_right_to_left_edge_case_level_greater_than_tree_height():
    root = make_tree()
    assert list(get_nodes_from_right_to_left(root, 4)) == []

def test_get_nodes_from_right_to_left_failure_invalid_level():
    root = make_tree()
    with pytest.raises(ValueError):
        list(get_nodes_from_right_to_left(root, 0))
```

Note: The `Node` class and `make_tree` function are assumed to be defined in the `data_structures.binary_tree.node` module, and the `make_tree` function is used to create a sample binary tree for testing purposes. Adjust the imports and tree creation as necessary based on your actual implementation.