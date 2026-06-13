import pytest
from data_structures.stacks.prefix_evaluation import evaluate

def test_evaluate_normal_cases():
    assert evaluate("+ 9 * 2 6") == 21
    assert evaluate("/ * 10 2 + 4 1") == 4.0
    assert evaluate("2") == 2
    assert evaluate("+ * 2 3 / 8 4") == 8.0

def test_evaluate_edge_cases():
    assert evaluate("+ 0 0") == 0
    assert evaluate("- 0 0") == 0
    assert evaluate("* 0 1") == 0
    assert evaluate("/ 1 1") == 1.0

def test_evaluate_single_operand():
    assert evaluate("42") == 42

def test_evaluate_invalid_expression():
    with pytest.raises(IndexError):
        evaluate("+ 1")  # Not enough operands

    with pytest.raises(KeyError):
        evaluate("? 1 2")  # Invalid operator

    with pytest.raises(ValueError):
        evaluate("+ a b")  # Non-numeric operand