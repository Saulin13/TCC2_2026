import pytest
from data_structures.stacks.next_greater_element import next_greatest_element

def test_next_greatest_element_normal_case():
    assert next_greatest_element([4, 5, 2, 25]) == [5, 25, 25, -1]
    assert next_greatest_element([13, 7, 6, 12]) == [-1, 12, 12, -1]

def test_next_greatest_element_edge_case_empty():
    assert next_greatest_element([]) == []

def test_next_greatest_element_edge_case_single_element():
    assert next_greatest_element([10]) == [-1]

def test_next_greatest_element_edge_case_all_same():
    assert next_greatest_element([5, 5, 5, 5]) == [-1, -1, -1, -1]

def test_next_greatest_element_edge_case_descending():
    assert next_greatest_element([9, 8, 7, 6]) == [-1, -1, -1, -1]

def test_next_greatest_element_edge_case_ascending():
    assert next_greatest_element([1, 2, 3, 4]) == [2, 3, 4, -1]

def test_next_greatest_element_failure_non_numeric():
    with pytest.raises(TypeError):
        next_greatest_element(['a', 'b', 'c'])

def test_next_greatest_element_mixed_numbers():
    assert next_greatest_element([1.5, 2.5, 0.5, 3.5]) == [2.5, 3.5, 3.5, -1]
    assert next_greatest_element([-1, -2, -3, 0]) == [0, 0, 0, -1]