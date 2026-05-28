import pytest
from data_structures.linked_list.is_palindrome import is_palindrome_stack

class ListNode:
    def __init__(self, val=0, next_node=None):
        self.val = val
        self.next_node = next_node

def test_is_palindrome_stack_empty_list():
    assert is_palindrome_stack(None) == True

def test_is_palindrome_stack_single_element():
    assert is_palindrome_stack(ListNode(1)) == True

def test_is_palindrome_stack_two_elements_palindrome():
    assert is_palindrome_stack(ListNode(1, ListNode(1))) == True

def test_is_palindrome_stack_two_elements_non_palindrome():
    assert is_palindrome_stack(ListNode(1, ListNode(2))) == False

def test_is_palindrome_stack_odd_length_palindrome():
    assert is_palindrome_stack(ListNode(1, ListNode(2, ListNode(1)))) == True

def test_is_palindrome_stack_even_length_palindrome():
    assert is_palindrome_stack(ListNode(1, ListNode(2, ListNode(2, ListNode(1))))) == True

def test_is_palindrome_stack_odd_length_non_palindrome():
    assert is_palindrome_stack(ListNode(1, ListNode(2, ListNode(3)))) == False

def test_is_palindrome_stack_even_length_non_palindrome():
    assert is_palindrome_stack(ListNode(1, ListNode(2, ListNode(3, ListNode(4))))) == False

def test_is_palindrome_stack_long_palindrome():
    assert is_palindrome_stack(ListNode(1, ListNode(2, ListNode(3, ListNode(2, ListNode(1)))))) == True

def test_is_palindrome_stack_long_non_palindrome():
    assert is_palindrome_stack(ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))) == False