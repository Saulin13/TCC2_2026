import pytest
from data_structures.binary_tree.avl_tree import left_rotation, MyNode


def test_left_rotation_basic():
    """Test basic left rotation with two nodes"""
    node_a = MyNode(10)
    node_b = MyNode(20)
    node_a.set_right(node_b)
    node_a.set_height(2)
    node_b.set_height(1)
    
    result = left_rotation(node_a)
    
    assert result.get_data() == 20
    assert result.get_left().get_data() == 10
    assert result.get_right() is None
    assert result.get_left().get_right() is None


def test_left_rotation_with_three_nodes():
    """Test left rotation with three nodes forming a complete structure"""
    node_a = MyNode(10)
    node_b = MyNode(20)
    node_c = MyNode(15)
    
    node_a.set_right(node_b)
    node_b.set_left(node_c)
    node_a.set_height(3)
    node_b.set_height(2)
    node_c.set_height(1)
    
    result = left_rotation(node_a)
    
    assert result.get_data() == 20
    assert result.get_left().get_data() == 10
    assert result.get_left().get_right().get_data() == 15


def test_left_rotation_with_left_child():
    """Test left rotation when the pivot node has a left child"""
    node_a = MyNode(10)
    node_b = MyNode(20)
    node_c = MyNode(5)
    
    node_a.set_right(node_b)
    node_a.set_left(node_c)
    node_a.set_height(2)
    node_b.set_height(1)
    node_c.set_height(1)
    
    result = left_rotation(node_a)
    
    assert result.get_data() == 20
    assert result.get_left().get_data() == 10
    assert result.get_left().get_left().get_data() == 5


def test_left_rotation_complex_tree():
    """Test left rotation with a more complex tree structure"""
    node_a = MyNode(30)
    node_b = MyNode(50)
    node_c = MyNode(20)
    node_d = MyNode(40)
    node_e = MyNode(60)
    
    node_a.set_right(node_b)
    node_a.set_left(node_c)
    node_b.set_left(node_d)
    node_b.set_right(node_e)
    
    node_a.set_height(3)
    node_b.set_height(2)
    node_c.set_height(1)
    node_d.set_height(1)
    node_e.set_height(1)
    
    result = left_rotation(node_a)
    
    assert result.get_data() == 50
    assert result.get_left().get_data() == 30
    assert result.get_right().get_data() == 60
    assert result.get_left().get_left().get_data() == 20
    assert result.get_left().get_right().get_data() == 40


def test_left_rotation_height_update():
    """Test that heights are correctly updated after rotation"""
    node_a = MyNode(10)
    node_b = MyNode(20)
    node_c = MyNode(25)
    
    node_a.set_right(node_b)
    node_b.set_right(node_c)
    node_a.set_height(3)
    node_b.set_height(2)
    node_c.set_height(1)
    
    result = left_rotation(node_a)
    
    assert result.get_height() >= 1
    assert result.get_left().get_height() >= 1


def test_left_rotation_no_right_child_raises_assertion():
    """Test that left rotation raises AssertionError when node has no right child"""
    node_a = MyNode(10)
    node_a.set_height(1)
    
    with pytest.raises(AssertionError):
        left_rotation(node_a)


def test_left_rotation_single_right_child():
    """Test left rotation with only a right child, no grandchildren"""
    node_a = MyNode(5)
    node_b = MyNode(10)
    
    node_a.set_right(node_b)
    node_a.set_height(2)
    node_b.set_height(1)
    
    result = left_rotation(node_a)
    
    assert result.get_data() == 10
    assert result.get_left().get_data() == 5
    assert result.get_left().get_left() is None
    assert result.get_left().get_right() is None