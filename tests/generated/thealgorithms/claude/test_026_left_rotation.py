import pytest
from data_structures.binary_tree.avl_tree import left_rotation, MyNode


def test_left_rotation_basic():
    """Test basic left rotation with simple tree structure."""
    node_a = MyNode(10)
    node_b = MyNode(20)
    node_c = MyNode(15)
    
    node_a.set_right(node_b)
    node_b.set_left(node_c)
    
    node_a.set_height(2)
    node_b.set_height(1)
    node_c.set_height(0)
    
    result = left_rotation(node_a)
    
    assert result.get_data() == 20
    assert result.get_left().get_data() == 10
    assert result.get_left().get_right().get_data() == 15


def test_left_rotation_with_no_left_child():
    """Test left rotation when right child has no left child."""
    node_a = MyNode(5)
    node_b = MyNode(10)
    
    node_a.set_right(node_b)
    node_a.set_height(1)
    node_b.set_height(0)
    
    result = left_rotation(node_a)
    
    assert result.get_data() == 10
    assert result.get_left().get_data() == 5
    assert result.get_left().get_right() is None


def test_left_rotation_with_complex_subtree():
    """Test left rotation with more complex subtree structure."""
    node_a = MyNode(30)
    node_b = MyNode(50)
    node_c = MyNode(40)
    node_d = MyNode(35)
    node_e = MyNode(45)
    
    node_a.set_right(node_b)
    node_b.set_left(node_c)
    node_c.set_left(node_d)
    node_c.set_right(node_e)
    
    node_a.set_height(3)
    node_b.set_height(2)
    node_c.set_height(1)
    node_d.set_height(0)
    node_e.set_height(0)
    
    result = left_rotation(node_a)
    
    assert result.get_data() == 50
    assert result.get_left().get_data() == 30
    assert result.get_left().get_right().get_data() == 40
    assert result.get_left().get_right().get_left().get_data() == 35
    assert result.get_left().get_right().get_right().get_data() == 45


def test_left_rotation_height_update():
    """Test that heights are correctly updated after rotation."""
    node_a = MyNode(1)
    node_b = MyNode(2)
    node_c = MyNode(3)
    
    node_a.set_right(node_b)
    node_b.set_right(node_c)
    
    node_a.set_height(2)
    node_b.set_height(1)
    node_c.set_height(0)
    
    result = left_rotation(node_a)
    
    assert result.get_height() == 1
    assert result.get_left().get_height() == 0


def test_left_rotation_with_left_subtree():
    """Test left rotation when original node has left subtree."""
    node_a = MyNode(20)
    node_left = MyNode(10)
    node_right = MyNode(30)
    node_mid = MyNode(25)
    
    node_a.set_left(node_left)
    node_a.set_right(node_right)
    node_right.set_left(node_mid)
    
    node_a.set_height(2)
    node_left.set_height(0)
    node_right.set_height(1)
    node_mid.set_height(0)
    
    result = left_rotation(node_a)
    
    assert result.get_data() == 30
    assert result.get_left().get_data() == 20
    assert result.get_left().get_left().get_data() == 10
    assert result.get_left().get_right().get_data() == 25


def test_left_rotation_no_right_child_raises_assertion():
    """Test that left rotation raises AssertionError when node has no right child."""
    node = MyNode(10)
    node.set_height(0)
    
    with pytest.raises(AssertionError):
        left_rotation(node)


def test_left_rotation_none_right_child_raises_assertion():
    """Test that left rotation raises AssertionError when right child is explicitly None."""
    node = MyNode(5)
    node.set_right(None)
    node.set_height(0)
    
    with pytest.raises(AssertionError):
        left_rotation(node)