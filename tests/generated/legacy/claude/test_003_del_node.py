import pytest
from data_structures.binary_tree.avl_tree import del_node, MyNode


def create_node(data, left=None, right=None):
    node = MyNode(data)
    if left:
        node.set_left(left)
    if right:
        node.set_right(right)
    return node


def test_del_node_leaf_node():
    root = create_node(10)
    result = del_node(root, 10)
    assert result is None


def test_del_node_with_only_left_child():
    left = create_node(5)
    root = create_node(10, left=left)
    result = del_node(root, 10)
    assert result is not None
    assert result.get_data() == 5
    assert result.get_left() is None
    assert result.get_right() is None


def test_del_node_with_only_right_child():
    right = create_node(15)
    root = create_node(10, right=right)
    result = del_node(root, 10)
    assert result is not None
    assert result.get_data() == 15
    assert result.get_left() is None
    assert result.get_right() is None


def test_del_node_with_two_children():
    left = create_node(5)
    right = create_node(15)
    root = create_node(10, left=left, right=right)
    result = del_node(root, 10)
    assert result is not None
    assert result.get_data() == 15
    assert result.get_left() is not None
    assert result.get_left().get_data() == 5
    assert result.get_right() is None


def test_del_node_left_subtree():
    left = create_node(5)
    right = create_node(15)
    root = create_node(10, left=left, right=right)
    result = del_node(root, 5)
    assert result is not None
    assert result.get_data() == 10
    assert result.get_left() is None
    assert result.get_right() is not None
    assert result.get_right().get_data() == 15


def test_del_node_right_subtree():
    left = create_node(5)
    right = create_node(15)
    root = create_node(10, left=left, right=right)
    result = del_node(root, 15)
    assert result is not None
    assert result.get_data() == 10
    assert result.get_left() is not None
    assert result.get_left().get_data() == 5
    assert result.get_right() is None


def test_del_node_not_found_left(capsys):
    right = create_node(15)
    root = create_node(10, right=right)
    result = del_node(root, 5)
    captured = capsys.readouterr()
    assert "No such data" in captured.out
    assert result is not None
    assert result.get_data() == 10


def test_del_node_not_found_right():
    left = create_node(5)
    root = create_node(10, left=left)
    result = del_node(root, 15)
    assert result is not None
    assert result.get_data() == 10
    assert result.get_left() is not None
    assert result.get_left().get_data() == 5


def test_del_node_complex_tree():
    node5 = create_node(5)
    node15 = create_node(15)
    node25 = create_node(25)
    node20 = create_node(20, left=node15, right=node25)
    root = create_node(10, left=node5, right=node20)
    
    result = del_node(root, 20)
    assert result is not None
    assert result.get_data() == 10
    assert result.get_right() is not None
    assert result.get_right().get_data() == 25


def test_del_node_triggers_rebalancing():
    node1 = create_node(1)
    node3 = create_node(3)
    node2 = create_node(2, left=node1, right=node3)
    node6 = create_node(6)
    node5 = create_node(5, right=node6)
    root = create_node(4, left=node2, right=node5)
    
    result = del_node(root, 1)
    assert result is not None
    assert result.get_data() == 4


def test_del_node_string_data():
    left = create_node("apple")
    right = create_node("cherry")
    root = create_node("banana", left=left, right=right)
    result = del_node(root, "apple")
    assert result is not None
    assert result.get_data() == "banana"
    assert result.get_left() is None
    assert result.get_right().get_data() == "cherry"