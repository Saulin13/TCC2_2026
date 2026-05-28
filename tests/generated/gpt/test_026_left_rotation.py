import pytest
from data_structures.binary_tree.avl_tree import left_rotation
from data_structures.binary_tree.avl_tree import MyNode, get_height, my_max

def test_left_rotation_normal_case():
    # Create nodes
    node = MyNode(10)
    right_child = MyNode(20)
    right_left_child = MyNode(15)

    # Set up the initial tree
    node.set_right(right_child)
    right_child.set_left(right_left_child)

    # Perform left rotation
    new_root = left_rotation(node)

    # Assertions
    assert new_root.get_data() == 20
    assert new_root.get_left().get_data() == 10
    assert new_root.get_left().get_right().get_data() == 15
    assert new_root.get_left().get_left() is None
    assert new_root.get_right() is None

def test_left_rotation_edge_case_single_node():
    # Create a single node
    node = MyNode(10)

    # Perform left rotation
    with pytest.raises(AssertionError):
        left_rotation(node)

def test_left_rotation_edge_case_no_right_child():
    # Create nodes
    node = MyNode(10)
    left_child = MyNode(5)

    # Set up the initial tree
    node.set_left(left_child)

    # Perform left rotation
    with pytest.raises(AssertionError):
        left_rotation(node)

def test_left_rotation_edge_case_right_child_no_left():
    # Create nodes
    node = MyNode(10)
    right_child = MyNode(20)

    # Set up the initial tree
    node.set_right(right_child)

    # Perform left rotation
    new_root = left_rotation(node)

    # Assertions
    assert new_root.get_data() == 20
    assert new_root.get_left().get_data() == 10
    assert new_root.get_left().get_left() is None
    assert new_root.get_left().get_right() is None
    assert new_root.get_right() is None