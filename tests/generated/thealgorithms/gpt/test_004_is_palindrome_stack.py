import pytest
from data_structures.linked_list.is_palindrome import is_palindrome_stack

class ListNode:
    def __init__(self, val=0, next_node=None):
        self.val = val
        self.next_node = next_node

@pytest.fixture
def create_linked_list():
    def _create_linked_list(values):
        if not values:
            return None
        head = ListNode(values[0])
        current = head
        for value in values[1:]:
            current.next_node = ListNode(value)
            current = current.next_node
        return head
    return _create_linked_list

def test_is_palindrome_stack_empty(create_linked_list):
    head = create_linked_list([])
    assert is_palindrome_stack(head) == True

def test_is_palindrome_stack_single_element(create_linked_list):
    head = create_linked_list([1])
    assert is_palindrome_stack(head) == True

def test_is_palindrome_stack_two_elements_palindrome(create_linked_list):
    head = create_linked_list([1, 1])
    assert is_palindrome_stack(head) == True

def test_is_palindrome_stack_two_elements_non_palindrome(create_linked_list):
    head = create_linked_list([1, 2])
    assert is_palindrome_stack(head) == False

def test_is_palindrome_stack_odd_elements_palindrome(create_linked_list):
    head = create_linked_list([1, 2, 1])
    assert is_palindrome_stack(head) == True

def test_is_palindrome_stack_even_elements_palindrome(create_linked_list):
    head = create_linked_list([1, 2, 2, 1])
    assert is_palindrome_stack(head) == True

def test_is_palindrome_stack_odd_elements_non_palindrome(create_linked_list):
    head = create_linked_list([1, 2, 3])
    assert is_palindrome_stack(head) == False

def test_is_palindrome_stack_even_elements_non_palindrome(create_linked_list):
    head = create_linked_list([1, 2, 3, 4])
    assert is_palindrome_stack(head) == False

def test_is_palindrome_stack_complex_palindrome(create_linked_list):
    head = create_linked_list([1, 2, 3, 2, 1])
    assert is_palindrome_stack(head) == True

def test_is_palindrome_stack_complex_non_palindrome(create_linked_list):
    head = create_linked_list([1, 2, 3, 4, 5])
    assert is_palindrome_stack(head) == False