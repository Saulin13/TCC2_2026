import pytest
from data_structures.binary_tree.avl_tree import left_rotation
from data_structures.binary_tree.avl_tree import MyNode, get_height, my_max

def test_left_rotation_normal_case():
    # Create nodes
    node = MyNode(10)
    right_child = MyNode(20)
    right_left_child = MyNode(15)

    # Set up the tree
    node.set_right(right_child)
    right_child.set_left(right_left_child)

    # Perform left rotation
    new_root = left_rotation(node)

    # Assertions
    assert new_root == right_child
    assert new_root.get_left() == node
    assert new_root.get_left().get_right() == right_left_child
    assert new_root.get_left().get_left() is None
    assert new_root.get_right() is None

def test_left_rotation_single_node():
    # Create a single node
    node = MyNode(10)

    # Perform left rotation
    with pytest.raises(AssertionError):
        left_rotation(node)

def test_left_rotation_no_right_child():
    # Create nodes
    node = MyNode(10)
    left_child = MyNode(5)

    # Set up the tree
    node.set_left(left_child)

    # Perform left rotation
    with pytest.raises(AssertionError):
        left_rotation(node)

def test_left_rotation_complex_tree():
    # Create nodes
    node = MyNode(10)
    right_child = MyNode(20)
    right_left_child = MyNode(15)
    right_right_child = MyNode(25)

    # Set up the tree
    node.set_right(right_child)
    right_child.set_left(right_left_child)
    right_child.set_right(right_right_child)

    # Perform left rotation
    new_root = left_rotation(node)

    # Assertions
    assert new_root == right_child
    assert new_root.get_left() == node
    assert new_root.get_right() == right_right_child
    assert new_root.get_left().get_right() == right_left_child
    assert new_root.get_left().get_left() is None

def test_left_rotation_update_heights():
    # Create nodes
    node = MyNode(10)
    right_child = MyNode(20)
    right_left_child = MyNode(15)

    # Set up the tree
    node.set_right(right_child)
    right_child.set_left(right_left_child)

    # Perform left rotation
    new_root = left_rotation(node)

    # Assertions for heights
    assert new_root.get_height() == 2
    assert new_root.get_left().get_height() == 1
    assert new_root.get_left().get_right().get_height() == 0