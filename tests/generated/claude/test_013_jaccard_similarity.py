import pytest
from maths.jaccard_similarity import jaccard_similarity


def test_jaccard_similarity_sets_basic():
    set_a = {'a', 'b', 'c', 'd', 'e'}
    set_b = {'c', 'd', 'e', 'f', 'h', 'i'}
    assert jaccard_similarity(set_a, set_b) == 0.375


def test_jaccard_similarity_identical_sets():
    set_a = {'a', 'b', 'c', 'd', 'e'}
    assert jaccard_similarity(set_a, set_a) == 1.0


def test_jaccard_similarity_identical_sets_alternative_union():
    set_a = {'a', 'b', 'c', 'd', 'e'}
    assert jaccard_similarity(set_a, set_a, True) == 0.5


def test_jaccard_similarity_lists():
    set_a = ['a', 'b', 'c', 'd', 'e']
    set_b = ['c', 'd', 'e', 'f', 'h', 'i']
    assert jaccard_similarity(set_a, set_b) == 0.375


def test_jaccard_similarity_list_and_tuple():
    set_a = ['a', 'b', 'c', 'd', 'e']
    set_b = ('c', 'd', 'e', 'f', 'h', 'i')
    assert jaccard_similarity(set_a, set_b) == 0.375


def test_jaccard_similarity_tuple_and_list():
    set_a = ('c', 'd', 'e', 'f', 'h', 'i')
    set_b = ['a', 'b', 'c', 'd', 'e']
    assert jaccard_similarity(set_a, set_b) == 0.375


def test_jaccard_similarity_tuple_and_list_alternative_union():
    set_a = ('c', 'd', 'e', 'f', 'h', 'i')
    set_b = ['a', 'b', 'c', 'd']
    assert jaccard_similarity(set_a, set_b, True) == 0.2


def test_jaccard_similarity_no_intersection_sets():
    set_a = {'a', 'b', 'c'}
    set_b = {'d', 'e', 'f'}
    assert jaccard_similarity(set_a, set_b) == 0.0


def test_jaccard_similarity_no_intersection_lists():
    set_a = ['a', 'b', 'c']
    set_b = ['d', 'e', 'f']
    assert jaccard_similarity(set_a, set_b) == 0.0


def test_jaccard_similarity_complete_overlap_sets():
    set_a = {'a', 'b', 'c'}
    set_b = {'a', 'b', 'c'}
    assert jaccard_similarity(set_a, set_b) == 1.0


def test_jaccard_similarity_complete_overlap_lists():
    set_a = ['a', 'b', 'c']
    set_b = ['a', 'b', 'c']
    assert jaccard_similarity(set_a, set_b) == 1.0


def test_jaccard_similarity_single_element_sets():
    set_a = {'a'}
    set_b = {'a'}
    assert jaccard_similarity(set_a, set_b) == 1.0


def test_jaccard_similarity_single_element_different_sets():
    set_a = {'a'}
    set_b = {'b'}
    assert jaccard_similarity(set_a, set_b) == 0.0


def test_jaccard_similarity_empty_intersection_alternative_union():
    set_a = {'a', 'b'}
    set_b = {'c', 'd'}
    assert jaccard_similarity(set_a, set_b, True) == 0.0


def test_jaccard_similarity_lists_with_duplicates():
    set_a = ['a', 'a', 'b', 'c']
    set_b = ['b', 'c', 'c', 'd']
    result = jaccard_similarity(set_a, set_b)
    assert result == 0.4


def test_jaccard_similarity_tuples():
    set_a = ('a', 'b', 'c')
    set_b = ('b', 'c', 'd')
    assert jaccard_similarity(set_a, set_b) == 0.5


def test_jaccard_similarity_sets_alternative_union():
    set_a = {'a', 'b', 'c'}
    set_b = {'c', 'd', 'e'}
    result = jaccard_similarity(set_a, set_b, True)
    assert result == pytest.approx(1/6, rel=1e-9)


def test_jaccard_similarity_mixed_types_raises_error():
    set_a = {'a', 'b'}
    set_b = ['c', 'd']
    with pytest.raises(ValueError) as excinfo:
        jaccard_similarity(set_a, set_b)
    assert "Set a and b must either both be sets or be either a list or a tuple." in str(excinfo.value)


def test_jaccard_similarity_set_and_tuple_raises_error():
    set_a = {'a', 'b'}
    set_b = ('c', 'd')
    with pytest.raises(ValueError) as excinfo:
        jaccard_similarity(set_a, set_b)
    assert "Set a and b must either both be sets or be either a list or a tuple." in str(excinfo.value)


def test_jaccard_similarity_list_and_set_raises_error():
    set_a = ['a', 'b']
    set_b = {'c', 'd'}
    with pytest.raises(ValueError) as excinfo:
        jaccard_similarity(set_a, set_b)
    assert "Set a and b must either both be sets or be either a list or a tuple." in str(excinfo.value)