import pytest
from data_structures.binary_tree.binary_tree_traversals import get_nodes_from_right_to_left


class Node:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right


def test_single_node_at_level_1():
    root = Node(5)
    result = list(get_nodes_from_right_to_left(root, 1))
    assert result == [5]


def test_two_levels_right_to_left():
    root = Node(1, Node(2), Node(3))
    result = list(get_nodes_from_right_to_left(root, 2))
    assert result == [3, 2]


def test_three_levels_complete_tree():
    root = Node(1, 
                Node(2, Node(4), Node(5)), 
                Node(3, Node(6), Node(7)))
    result = list(get_nodes_from_right_to_left(root, 3))
    assert result == [7, 6, 5, 4]


def test_three_levels_root_level():
    root = Node(1, 
                Node(2, Node(4), Node(5)), 
                Node(3, Node(6), Node(7)))
    result = list(get_nodes_from_right_to_left(root, 1))
    assert result == [1]


def test_three_levels_middle_level():
    root = Node(1, 
                Node(2, Node(4), Node(5)), 
                Node(3, Node(6), Node(7)))
    result = list(get_nodes_from_right_to_left(root, 2))
    assert result == [3, 2]


def test_empty_tree():
    result = list(get_nodes_from_right_to_left(None, 1))
    assert result == []


def test_level_greater_than_tree_depth():
    root = Node(1, Node(2), Node(3))
    result = list(get_nodes_from_right_to_left(root, 5))
    assert result == []


def test_level_zero():
    root = Node(1, Node(2), Node(3))
    result = list(get_nodes_from_right_to_left(root, 0))
    assert result == []


def test_unbalanced_tree_left_heavy():
    root = Node(1, Node(2, Node(4, Node(8))), Node(3))
    result = list(get_nodes_from_right_to_left(root, 4))
    assert result == [8]


def test_unbalanced_tree_right_heavy():
    root = Node(1, Node(2), Node(3, None, Node(7, None, Node(9))))
    result = list(get_nodes_from_right_to_left(root, 4))
    assert result == [9]


def test_only_left_children():
    root = Node(1, Node(2, Node(3)))
    result = list(get_nodes_from_right_to_left(root, 3))
    assert result == [3]


def test_only_right_children():
    root = Node(1, None, Node(2, None, Node(3)))
    result = list(get_nodes_from_right_to_left(root, 3))
    assert result == [3]


def test_sparse_tree_with_gaps():
    root = Node(1, Node(2, None, Node(5)), Node(3, Node(6)))
    result = list(get_nodes_from_right_to_left(root, 3))
    assert result == [6, 5]


def test_negative_level():
    root = Node(1, Node(2), Node(3))
    result = list(get_nodes_from_right_to_left(root, -1))
    assert result == []


def test_large_values():
    root = Node(1000, Node(2000, Node(4000)), Node(3000, None, Node(7000)))
    result = list(get_nodes_from_right_to_left(root, 3))
    assert result == [7000, 4000]


def test_duplicate_values():
    root = Node(5, Node(5, Node(5)), Node(5, Node(5)))
    result = list(get_nodes_from_right_to_left(root, 3))
    assert result == [5, 5]