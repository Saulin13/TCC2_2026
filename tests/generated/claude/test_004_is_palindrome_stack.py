import pytest
from data_structures.linked_list.is_palindrome import is_palindrome_stack


class ListNode:
    def __init__(self, val=0, next_node=None):
        self.val = val
        self.next_node = next_node


def test_is_palindrome_stack_none():
    assert is_palindrome_stack(None) is True


def test_is_palindrome_stack_single_node():
    head = ListNode(1)
    assert is_palindrome_stack(head) is True


def test_is_palindrome_stack_two_nodes_not_palindrome():
    head = ListNode(1, ListNode(2))
    assert is_palindrome_stack(head) is False


def test_is_palindrome_stack_two_nodes_palindrome():
    head = ListNode(1, ListNode(1))
    assert is_palindrome_stack(head) is True


def test_is_palindrome_stack_three_nodes_palindrome():
    head = ListNode(1, ListNode(2, ListNode(1)))
    assert is_palindrome_stack(head) is True


def test_is_palindrome_stack_three_nodes_not_palindrome():
    head = ListNode(1, ListNode(2, ListNode(3)))
    assert is_palindrome_stack(head) is False


def test_is_palindrome_stack_four_nodes_palindrome():
    head = ListNode(1, ListNode(2, ListNode(2, ListNode(1))))
    assert is_palindrome_stack(head) is True


def test_is_palindrome_stack_four_nodes_not_palindrome():
    head = ListNode(1, ListNode(2, ListNode(3, ListNode(4))))
    assert is_palindrome_stack(head) is False


def test_is_palindrome_stack_five_nodes_palindrome():
    head = ListNode(1, ListNode(2, ListNode(3, ListNode(2, ListNode(1)))))
    assert is_palindrome_stack(head) is True


def test_is_palindrome_stack_five_nodes_not_palindrome():
    head = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))
    assert is_palindrome_stack(head) is False


def test_is_palindrome_stack_six_nodes_palindrome():
    head = ListNode(1, ListNode(2, ListNode(3, ListNode(3, ListNode(2, ListNode(1))))))
    assert is_palindrome_stack(head) is True


def test_is_palindrome_stack_six_nodes_not_palindrome():
    head = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5, ListNode(6))))))
    assert is_palindrome_stack(head) is False


def test_is_palindrome_stack_with_negative_values():
    head = ListNode(-1, ListNode(0, ListNode(-1)))
    assert is_palindrome_stack(head) is True


def test_is_palindrome_stack_with_zero_values():
    head = ListNode(0, ListNode(0, ListNode(0)))
    assert is_palindrome_stack(head) is True


def test_is_palindrome_stack_long_palindrome():
    head = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5, ListNode(4, ListNode(3, ListNode(2, ListNode(1)))))))))
    assert is_palindrome_stack(head) is True


def test_is_palindrome_stack_long_not_palindrome():
    head = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5, ListNode(6, ListNode(7, ListNode(8, ListNode(9)))))))))
    assert is_palindrome_stack(head) is False


def test_is_palindrome_stack_repeated_values_palindrome():
    head = ListNode(5, ListNode(5, ListNode(5, ListNode(5))))
    assert is_palindrome_stack(head) is True


def test_is_palindrome_stack_almost_palindrome():
    head = ListNode(1, ListNode(2, ListNode(3, ListNode(2, ListNode(2)))))
    assert is_palindrome_stack(head) is False