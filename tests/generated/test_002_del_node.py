import pytest
from data_structures.binary_tree.avl_tree import del_node
from data_structures.binary_tree.avl_tree import MyNode, get_left_most, get_height, left_rotation, rl_rotation, right_rotation, lr_rotation, my_max

def create_avl_tree():
    # Helper function to create a sample AVL tree
    root = MyNode(10)
    root.set_left(MyNode(5))
    root.set_right(MyNode(15))
    root.get_left().set_left(MyNode(3))
    root.get_left().set_right(MyNode(7))
    root.get_right().set_left(MyNode(12))
    root.get_right().set_right(MyNode(18))
    return root

def test_del_node_normal_case():
    root = create_avl_tree()
    new_root = del_node(root, 5)
    assert new_root.get_data() == 10
    assert new_root.get_left().get_data() == 7
    assert new_root.get_left().get_left().get_data() == 3

def test_del_node_leaf_node():
    root = create_avl_tree()
    new_root = del_node(root, 3)
    assert new_root.get_data() == 10
    assert new_root.get_left().get_data() == 5
    assert new_root.get_left().get_left() is None

def test_del_node_root_node():
    root = create_avl_tree()
    new_root = del_node(root, 10)
    assert new_root.get_data() == 12
    assert new_root.get_right().get_data() == 15

def test_del_node_non_existent():
    root = create_avl_tree()
    new_root = del_node(root, 100)
    assert new_root.get_data() == 10
    assert new_root.get_right().get_right().get_data() == 18

def test_del_node_single_node_tree():
    root = MyNode(10)
    new_root = del_node(root, 10)
    assert new_root is None

def test_del_node_empty_tree():
    new_root = del_node(None, 10)
    assert new_root is None

def test_del_node_causes_rotation():
    root = MyNode(30)
    root.set_left(MyNode(20))
    root.set_right(MyNode(40))
    root.get_left().set_left(MyNode(10))
    root.get_left().set_right(MyNode(25))
    root.get_left().get_left().set_left(MyNode(5))
    
    new_root = del_node(root, 40)
    assert new_root.get_data() == 20
    assert new_root.get_right().get_data() == 30
    assert new_root.get_left().get_data() == 10