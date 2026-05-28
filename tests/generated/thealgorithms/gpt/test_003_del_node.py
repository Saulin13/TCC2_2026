import pytest
from data_structures.binary_tree.avl_tree import del_node
from data_structures.binary_tree.avl_tree import MyNode, get_left_most, get_height, left_rotation, rl_rotation, right_rotation, lr_rotation, my_max

@pytest.fixture
def avl_tree():
    # Create a simple AVL tree for testing
    root = MyNode(10)
    root.set_left(MyNode(5))
    root.set_right(MyNode(15))
    root.get_left().set_left(MyNode(3))
    root.get_left().set_right(MyNode(7))
    root.get_right().set_left(MyNode(13))
    root.get_right().set_right(MyNode(17))
    return root

def test_del_node_normal_case(avl_tree):
    # Test deleting a node with two children
    root = del_node(avl_tree, 10)
    assert root.get_data() != 10
    assert root.get_left().get_data() == 5
    assert root.get_right().get_data() == 15

def test_del_node_leaf(avl_tree):
    # Test deleting a leaf node
    root = del_node(avl_tree, 3)
    assert root.get_left().get_left() is None

def test_del_node_single_child(avl_tree):
    # Test deleting a node with a single child
    root = del_node(avl_tree, 5)
    assert root.get_left().get_data() == 7

def test_del_node_non_existent(avl_tree):
    # Test deleting a non-existent node
    root = del_node(avl_tree, 100)
    assert root.get_data() == 10
    assert root.get_right().get_right().get_data() == 17

def test_del_node_empty_tree():
    # Test deleting from an empty tree
    root = del_node(None, 10)
    assert root is None