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


def test_two_levels_at_level_1():
    root = Node(1, Node(2), Node(3))
    result = list(get_nodes_from_right_to_left(root, 1))
    assert result == [1]


def test_two_levels_at_level_2():
    root = Node(1, Node(2), Node(3))
    result = list(get_nodes_from_right_to_left(root, 2))
    assert result == [3, 2]


def test_three_levels_complete_tree():
    root = Node(1, 
                Node(2, Node(4), Node(5)), 
                Node(3, Node(6), Node(7)))
    result = list(get_nodes_from_right_to_left(root, 3))
    assert result == [7, 6, 5, 4]


def test_three_levels_at_level_2():
    root = Node(1, 
                Node(2, Node(4), Node(5)), 
                Node(3, Node(6), Node(7)))
    result = list(get_nodes_from_right_to_left(root, 2))
    assert result == [3, 2]


def test_unbalanced_tree_left_heavy():
    root = Node(1, Node(2, Node(4)), None)
    result = list(get_nodes_from_right_to_left(root, 3))
    assert result == [4]


def test_unbalanced_tree_right_heavy():
    root = Node(1, None, Node(3, None, Node(7)))
    result = list(get_nodes_from_right_to_left(root, 3))
    assert result == [7]


def test_unbalanced_tree_mixed():
    root = Node(1, Node(2), Node(3, None, Node(7)))
    result = list(get_nodes_from_right_to_left(root, 3))
    assert result == [7]


def test_level_beyond_tree_depth():
    root = Node(1, Node(2), Node(3))
    result = list(get_nodes_from_right_to_left(root, 5))
    assert result == []


def test_empty_tree():
    result = list(get_nodes_from_right_to_left(None, 1))
    assert result == []


def test_empty_tree_with_higher_level():
    result = list(get_nodes_from_right_to_left(None, 3))
    assert result == []


def test_level_zero():
    root = Node(1, Node(2), Node(3))
    result = list(get_nodes_from_right_to_left(root, 0))
    assert result == []


def test_negative_level():
    root = Node(1, Node(2), Node(3))
    result = list(get_nodes_from_right_to_left(root, -1))
    assert result == []


def test_large_tree_deep_level():
    root = Node(1,
                Node(2, 
                     Node(4, Node(8), Node(9)),
                     Node(5, Node(10), Node(11))),
                Node(3,
                     Node(6, Node(12), Node(13)),
                     Node(7, Node(14), Node(15))))
    result = list(get_nodes_from_right_to_left(root, 4))
    assert result == [15, 14, 13, 12, 11, 10, 9, 8]


def test_nodes_with_same_values():
    root = Node(5, Node(5, Node(5), Node(5)), Node(5, Node(5), Node(5)))
    result = list(get_nodes_from_right_to_left(root, 3))
    assert result == [5, 5, 5, 5]


def test_single_child_nodes_only_left():
    root = Node(1, Node(2, Node(3)), None)
    result = list(get_nodes_from_right_to_left(root, 2))
    assert result == [2]


def test_single_child_nodes_only_right():
    root = Node(1, None, Node(3, None, Node(4)))
    result = list(get_nodes_from_right_to_left(root, 2))
    assert result == [3]


def test_negative_node_values():
    root = Node(-1, Node(-2), Node(-3))
    result = list(get_nodes_from_right_to_left(root, 2))
    assert result == [-3, -2]