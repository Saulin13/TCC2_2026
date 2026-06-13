import pytest
from data_structures.stacks.prefix_evaluation import evaluate


def test_evaluate_addition():
    assert evaluate("+ 9 * 2 6") == 21


def test_evaluate_division():
    assert evaluate("/ * 10 2 + 4 1") == 4.0


def test_evaluate_single_operand():
    assert evaluate("2") == 2


def test_evaluate_complex_expression():
    assert evaluate("+ * 2 3 / 8 4") == 8.0


def test_evaluate_subtraction():
    assert evaluate("- 10 5") == 5


def test_evaluate_multiplication():
    assert evaluate("* 3 4") == 12


def test_evaluate_nested_operations():
    assert evaluate("* + 2 3 - 8 3") == 25


def test_evaluate_with_negative_result():
    assert evaluate("- 5 10") == -5


def test_evaluate_division_with_float_result():
    assert evaluate("/ 7 2") == 3.5


def test_evaluate_multiple_additions():
    assert evaluate("+ + 1 2 3") == 6


def test_evaluate_multiple_multiplications():
    assert evaluate("* * 2 3 4") == 24


def test_evaluate_zero_operand():
    assert evaluate("+ 0 5") == 5


def test_evaluate_with_extra_spaces():
    assert evaluate("+ 1 2 ") == 3


def test_evaluate_complex_nested():
    assert evaluate("- * / 15 3 2 + 1 1") == 8


def test_evaluate_invalid_expression_insufficient_operands():
    with pytest.raises(IndexError):
        evaluate("+ 5")


def test_evaluate_invalid_expression_too_many_operands():
    with pytest.raises(Exception):
        evaluate("5 6 7")


def test_evaluate_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        evaluate("/ 5 0")