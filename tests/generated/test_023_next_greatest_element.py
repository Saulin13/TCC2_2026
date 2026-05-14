import pytest
from data_structures.stacks.next_greater_element import next_greatest_element

def test_next_greatest_element_normal_case():
    assert next_greatest_element([4, 5, 2, 25]) == [5, 25, 25, -1]
    assert next_greatest_element([13, 7, 6, 12]) == [-1, 12, 12, -1]
    assert next_greatest_element([11, 13, 21, 3]) == [13, 21, -1, -1]

def test_next_greatest_element_edge_cases():
    assert next_greatest_element([]) == []
    assert next_greatest_element([10]) == [-1]
    assert next_greatest_element([10, 10, 10]) == [-1, -1, -1]
    assert next_greatest_element([1, 2, 3, 4, 5]) == [2, 3, 4, 5, -1]
    assert next_greatest_element([5, 4, 3, 2, 1]) == [-1, -1, -1, -1, -1]

def test_next_greatest_element_with_negative_numbers():
    assert next_greatest_element([-1, -2, -3, -4]) == [-1, -1, -1, -1]
    assert next_greatest_element([-4, -3, -2, -1]) == [-3, -2, -1, -1]
    assert next_greatest_element([-1, 0, 1]) == [0, 1, -1]

def test_next_greatest_element_with_floats():
    assert next_greatest_element([1.1, 2.2, 3.3, 2.2]) == [2.2, 3.3, -1, -1]
    assert next_greatest_element([3.3, 2.2, 1.1]) == [-1, -1, -1]

def test_next_greatest_element_failure_case():
    with pytest.raises(TypeError):
        next_greatest_element(None)