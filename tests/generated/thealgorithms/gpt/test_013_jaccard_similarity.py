import pytest
from maths.jaccard_similarity import jaccard_similarity

def test_jaccard_similarity_normal_case_sets():
    set_a = {'a', 'b', 'c', 'd', 'e'}
    set_b = {'c', 'd', 'e', 'f', 'h', 'i'}
    assert jaccard_similarity(set_a, set_b) == 0.375

def test_jaccard_similarity_identical_sets():
    set_a = {'a', 'b', 'c', 'd', 'e'}
    assert jaccard_similarity(set_a, set_a) == 1.0

def test_jaccard_similarity_identical_sets_alternative_union():
    set_a = {'a', 'b', 'c', 'd', 'e'}
    assert jaccard_similarity(set_a, set_a, True) == 0.5

def test_jaccard_similarity_normal_case_lists():
    set_a = ['a', 'b', 'c', 'd', 'e']
    set_b = ['c', 'd', 'e', 'f', 'h', 'i']
    assert jaccard_similarity(set_a, set_b) == 0.375

def test_jaccard_similarity_normal_case_tuples():
    set_a = ('c', 'd', 'e', 'f', 'h', 'i')
    set_b = ('a', 'b', 'c', 'd', 'e')
    assert jaccard_similarity(set_a, set_b) == 0.375

def test_jaccard_similarity_mixed_types():
    set_a = ('c', 'd', 'e', 'f', 'h', 'i')
    set_b = ['a', 'b', 'c', 'd']
    assert jaccard_similarity(set_a, set_b, True) == 0.2

def test_jaccard_similarity_empty_intersection():
    set_a = {'a', 'b'}
    set_b = ['c', 'd']
    with pytest.raises(ValueError, match="Set a and b must either both be sets or be either a list or a tuple."):
        jaccard_similarity(set_a, set_b)

def test_jaccard_similarity_no_intersection():
    set_a = {'x', 'y'}
    set_b = {'a', 'b'}
    assert jaccard_similarity(set_a, set_b) == 0.0

def test_jaccard_similarity_no_intersection_alternative_union():
    set_a = ['x', 'y']
    set_b = ['a', 'b']
    assert jaccard_similarity(set_a, set_b, True) == 0.0