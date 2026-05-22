import pytest
from maths.jaccard_similarity import jaccard_similarity

def test_jaccard_similarity_normal_case_sets():
    set_a = {'a', 'b', 'c', 'd', 'e'}
    set_b = {'c', 'd', 'e', 'f', 'h', 'i'}
    assert jaccard_similarity(set_a, set_b) == 0.375

def test_jaccard_similarity_normal_case_lists():
    list_a = ['a', 'b', 'c', 'd', 'e']
    list_b = ['c', 'd', 'e', 'f', 'h', 'i']
    assert jaccard_similarity(list_a, list_b) == 0.375

def test_jaccard_similarity_normal_case_tuples():
    tuple_a = ('a', 'b', 'c', 'd', 'e')
    tuple_b = ('c', 'd', 'e', 'f', 'h', 'i')
    assert jaccard_similarity(tuple_a, tuple_b) == 0.375

def test_jaccard_similarity_identical_sets():
    set_a = {'a', 'b', 'c'}
    assert jaccard_similarity(set_a, set_a) == 1.0

def test_jaccard_similarity_identical_lists():
    list_a = ['a', 'b', 'c']
    assert jaccard_similarity(list_a, list_a) == 1.0

def test_jaccard_similarity_identical_tuples():
    tuple_a = ('a', 'b', 'c')
    assert jaccard_similarity(tuple_a, tuple_a) == 1.0

def test_jaccard_similarity_alternative_union_sets():
    set_a = {'a', 'b', 'c'}
    set_b = {'c', 'd', 'e'}
    assert jaccard_similarity(set_a, set_b, True) == 0.2

def test_jaccard_similarity_alternative_union_lists():
    list_a = ['a', 'b', 'c']
    list_b = ['c', 'd', 'e']
    assert jaccard_similarity(list_a, list_b, True) == 0.2

def test_jaccard_similarity_alternative_union_tuples():
    tuple_a = ('a', 'b', 'c')
    tuple_b = ('c', 'd', 'e')
    assert jaccard_similarity(tuple_a, tuple_b, True) == 0.2

def test_jaccard_similarity_empty_intersection():
    set_a = {'a', 'b'}
    set_b = {'c', 'd'}
    assert jaccard_similarity(set_a, set_b) == 0.0

def test_jaccard_similarity_mixed_types_raises_value_error():
    set_a = {'a', 'b'}
    list_b = ['c', 'd']
    with pytest.raises(ValueError, match="Set a and b must either both be sets or be either a list or a tuple."):
        jaccard_similarity(set_a, list_b)