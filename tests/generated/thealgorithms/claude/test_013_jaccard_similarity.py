import pytest
from maths.jaccard_similarity import jaccard_similarity


def test_jaccard_similarity_sets_basic():
    set_a = {'a', 'b', 'c', 'd', 'e'}
    set_b = {'c', 'd', 'e', 'f', 'h', 'i'}
    assert jaccard_similarity(set_a, set_b) == 0.375


def test_jaccard_similarity_sets_identical():
    set_a = {'a', 'b', 'c', 'd', 'e'}
    assert jaccard_similarity(set_a, set_a) == 1.0


def test_jaccard_similarity_sets_identical_alternative_union():
    set_a = {'a', 'b', 'c', 'd', 'e'}
    assert jaccard_similarity(set_a, set_a, True) == 0.5


def test_jaccard_similarity_sets_no_intersection():
    set_a = {'a', 'b', 'c'}
    set_b = {'d', 'e', 'f'}
    assert jaccard_similarity(set_a, set_b) == 0.0


def test_jaccard_similarity_sets_alternative_union():
    set_a = {'a', 'b', 'c'}
    set_b = {'c', 'd', 'e'}
    intersection_length = 1
    union_length = 3 + 3
    expected = intersection_length / union_length
    assert jaccard_similarity(set_a, set_b, True) == expected


def test_jaccard_similarity_lists_basic():
    set_a = ['a', 'b', 'c', 'd', 'e']
    set_b = ['c', 'd', 'e', 'f', 'h', 'i']
    assert jaccard_similarity(set_a, set_b) == 0.375


def test_jaccard_similarity_tuples_basic():
    set_a = ('c', 'd', 'e', 'f', 'h', 'i')
    set_b = ('a', 'b', 'c', 'd', 'e')
    assert jaccard_similarity(set_a, set_b) == 0.375


def test_jaccard_similarity_list_and_tuple():
    set_a = ['a', 'b', 'c', 'd', 'e']
    set_b = ('c', 'd', 'e', 'f', 'h', 'i')
    assert jaccard_similarity(set_a, set_b) == 0.375


def test_jaccard_similarity_tuple_and_list():
    set_a = ('c', 'd', 'e', 'f', 'h', 'i')
    set_b = ['a', 'b', 'c', 'd', 'e']
    assert jaccard_similarity(set_a, set_b) == 0.375


def test_jaccard_similarity_lists_alternative_union():
    set_a = ('c', 'd', 'e', 'f', 'h', 'i')
    set_b = ['a', 'b', 'c', 'd']
    assert jaccard_similarity(set_a, set_b, True) == 0.2


def test_jaccard_similarity_lists_identical():
    set_a = ['a', 'b', 'c']
    assert jaccard_similarity(set_a, set_a) == 1.0


def test_jaccard_similarity_lists_no_intersection():
    set_a = ['a', 'b', 'c']
    set_b = ['d', 'e', 'f']
    assert jaccard_similarity(set_a, set_b) == 0.0


def test_jaccard_similarity_lists_with_duplicates():
    set_a = ['a', 'b', 'c', 'c']
    set_b = ['c', 'd', 'e']
    intersection = ['c', 'c']
    union = ['a', 'b', 'c', 'c', 'd', 'e']
    expected = len(intersection) / len(union)
    assert jaccard_similarity(set_a, set_b) == expected


def test_jaccard_similarity_empty_sets():
    set_a = set()
    set_b = set()
    with pytest.raises(ZeroDivisionError):
        jaccard_similarity(set_a, set_b)


def test_jaccard_similarity_empty_lists():
    set_a = []
    set_b = []
    with pytest.raises(ZeroDivisionError):
        jaccard_similarity(set_a, set_b)


def test_jaccard_similarity_one_empty_set():
    set_a = {'a', 'b', 'c'}
    set_b = set()
    assert jaccard_similarity(set_a, set_b) == 0.0


def test_jaccard_similarity_one_empty_list():
    set_a = ['a', 'b', 'c']
    set_b = []
    assert jaccard_similarity(set_a, set_b) == 0.0


def test_jaccard_similarity_set_and_list_raises_error():
    set_a = {'a', 'b'}
    set_b = ['c', 'd']
    with pytest.raises(ValueError) as exc_info:
        jaccard_similarity(set_a, set_b)
    assert "Set a and b must either both be sets or be either a list or a tuple." in str(exc_info.value)


def test_jaccard_similarity_set_and_tuple_raises_error():
    set_a = {'a', 'b'}
    set_b = ('c', 'd')
    with pytest.raises(ValueError) as exc_info:
        jaccard_similarity(set_a, set_b)
    assert "Set a and b must either both be sets or be either a list or a tuple." in str(exc_info.value)


def test_jaccard_similarity_invalid_types():
    set_a = "abc"
    set_b = "def"
    with pytest.raises(ValueError) as exc_info:
        jaccard_similarity(set_a, set_b)
    assert "Set a and b must either both be sets or be either a list or a tuple." in str(exc_info.value)


def test_jaccard_similarity_single_element_sets():
    set_a = {'a'}
    set_b = {'a'}
    assert jaccard_similarity(set_a, set_b) == 1.0


def test_jaccard_similarity_single_element_lists():
    set_a = ['a']
    set_b = ['b']
    assert jaccard_similarity(set_a, set_b) == 0.0