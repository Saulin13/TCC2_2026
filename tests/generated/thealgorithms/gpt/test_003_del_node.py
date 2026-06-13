import pytest
from data_structures.binary_tree.avl_tree import del_node

class MyNode:
    def __init__(self, data, left=None, right=None, height=1):
        self.data = data
        self.left = left
        self.right = right
        self.height = height

    def get_data(self):
        return self.data

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def set_data(self, data):
        self.data = data

    def set_left(self, left):
        self.left = left

    def set_right(self, right):
        self.right = right

    def set_height(self, height):
        self.height = height

def get_left_most(node):
    while node.get_left() is not None:
        node = node.get_left()
    return node.get_data()

def get_height(node):
    if node is None:
        return 0
    return node.height

def left_rotation(node):
    right_child = node.get_right()
    node.set_right(right_child.get_left())
    right_child.set_left(node)
    node.set_height(my_max(get_height(node.get_left()), get_height(node.get_right())) + 1)
    right_child.set_height(my_max(get_height(right_child.get_left()), get_height(right_child.get_right())) + 1)
    return right_child

def right_rotation(node):
    left_child = node.get_left()
    node.set_left(left_child.get_right())
    left_child.set_right(node)
    node.set_height(my_max(get_height(node.get_left()), get_height(node.get_right())) + 1)
    left_child.set_height(my_max(get_height(left_child.get_left()), get_height(left_child.get_right())) + 1)
    return left_child

def rl_rotation(node):
    node.set_right(right_rotation(node.get_right()))
    return left_rotation(node)

def lr_rotation(node):
    node.set_left(left_rotation(node.get_left()))
    return right_rotation(node)

def my_max(a, b):
    return a if a > b else b

@pytest.fixture
def avl_tree():
    # Create a simple AVL tree for testing
    node1 = MyNode(1)
    node3 = MyNode(3)
    node2 = MyNode(2, node1, node3)
    node5 = MyNode(5)
    node4 = MyNode(4, node2, node5)
    return node4

def test_del_node_normal_case(avl_tree):
    # Delete a node with two children
    new_root = del_node(avl_tree, 2)
    assert new_root.get_data() == 4
    assert new_root.get_left().get_data() == 3
    assert new_root.get_left().get_left().get_data() == 1

def test_del_node_leaf(avl_tree):
    # Delete a leaf node
    new_root = del_node(avl_tree, 1)
    assert new_root.get_left().get_left() is None

def test_del_node_single_child(avl_tree):
    # Delete a node with a single child
    new_root = del_node(avl_tree, 5)
    assert new_root.get_right() is None

def test_del_node_non_existent(avl_tree):
    # Attempt to delete a non-existent node
    new_root = del_node(avl_tree, 10)
    assert new_root.get_data() == 4
    assert new_root.get_left().get_data() == 2
    assert new_root.get_right().get_data() == 5

def test_del_node_empty_tree():
    # Attempt to delete from an empty tree
    new_root = del_node(None, 1)
    assert new_root is None