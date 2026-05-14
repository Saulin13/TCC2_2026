import pytest
from data_structures.linked_list.is_palindrome import is_palindrome_stack

class ListNode:
    def __init__(self, val=0, next_node=None):
        self.val = val
        self.next_node = next_node

@pytest.fixture
def linked_list():
    def _linked_list(values):
        if not values:
            return None
        head = ListNode(values[0])
        current = head
        for value in values[1:]:
            current.next_node = ListNode(value)
            current = current.next_node
        return head
    return _linked_list

def test_is_palindrome_stack_empty(linked_list):
    assert is_palindrome_stack(linked_list([])) == True

def test_is_palindrome_stack_single_element(linked_list):
    assert is_palindrome_stack(linked_list([1])) == True

def test_is_palindrome_stack_two_different_elements(linked_list):
    assert is_palindrome_stack(linked_list([1, 2])) == False

def test_is_palindrome_stack_two_same_elements(linked_list):
    assert is_palindrome_stack(linked_list([1, 1])) == True

def test_is_palindrome_stack_odd_palindrome(linked_list):
    assert is_palindrome_stack(linked_list([1, 2, 1])) == True

def test_is_palindrome_stack_even_palindrome(linked_list):
    assert is_palindrome_stack(linked_list([1, 2, 2, 1])) == True

def test_is_palindrome_stack_not_palindrome(linked_list):
    assert is_palindrome_stack(linked_list([1, 2, 3])) == False

def test_is_palindrome_stack_long_palindrome(linked_list):
    assert is_palindrome_stack(linked_list([1, 2, 3, 2, 1])) == True

def test_is_palindrome_stack_long_not_palindrome(linked_list):
    assert is_palindrome_stack(linked_list([1, 2, 3, 4, 5])) == False