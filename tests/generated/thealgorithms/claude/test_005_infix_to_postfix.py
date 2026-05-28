import pytest
from data_structures.stacks.infix_to_postfix_conversion import infix_to_postfix


def test_infix_to_postfix_empty_string():
    assert infix_to_postfix("") == ""


def test_infix_to_postfix_simple_addition():
    assert infix_to_postfix("3+2") == "3 2 +"


def test_infix_to_postfix_simple_subtraction():
    assert infix_to_postfix("5-3") == "5 3 -"


def test_infix_to_postfix_simple_multiplication():
    assert infix_to_postfix("4*2") == "4 2 *"


def test_infix_to_postfix_simple_division():
    assert infix_to_postfix("8/4") == "8 4 /"


def test_infix_to_postfix_with_parentheses():
    assert infix_to_postfix("(3+4)*5-6") == "3 4 + 5 * 6 -"


def test_infix_to_postfix_complex_expression():
    assert infix_to_postfix("(1+2)*3/4-5") == "1 2 + 3 * 4 / 5 -"


def test_infix_to_postfix_with_variables():
    assert infix_to_postfix("a+b*c+(d*e+f)*g") == "a b c * + d e * f + g * +"


def test_infix_to_postfix_with_exponentiation():
    assert infix_to_postfix("x^y/(5*z)+2") == "x y ^ 5 z * / 2 +"


def test_infix_to_postfix_right_associative_exponentiation():
    assert infix_to_postfix("2^3^2") == "2 3 2 ^ ^"


def test_infix_to_postfix_nested_parentheses():
    assert infix_to_postfix("((a+b)*c)") == "a b + c *"


def test_infix_to_postfix_multiple_operators():
    assert infix_to_postfix("a+b-c*d/e") == "a b + c d * e / -"


def test_infix_to_postfix_single_operand():
    assert infix_to_postfix("5") == "5"


def test_infix_to_postfix_single_variable():
    assert infix_to_postfix("x") == "x"


def test_infix_to_postfix_parentheses_only_addition():
    assert infix_to_postfix("(a+b)") == "a b +"


def test_infix_to_postfix_mismatched_parentheses_extra_closing():
    with pytest.raises(ValueError, match="Mismatched parentheses"):
        infix_to_postfix("(1*(2+3)+4))")


def test_infix_to_postfix_mismatched_parentheses_extra_opening():
    with pytest.raises(ValueError, match="Mismatched parentheses"):
        infix_to_postfix("((1+2)*3")


def test_infix_to_postfix_mismatched_parentheses_only_opening():
    with pytest.raises(ValueError, match="Mismatched parentheses"):
        infix_to_postfix("(((")


def test_infix_to_postfix_mismatched_parentheses_only_closing():
    with pytest.raises(ValueError, match="Mismatched parentheses"):
        infix_to_postfix(")))")


def test_infix_to_postfix_operator_precedence():
    assert infix_to_postfix("a+b*c") == "a b c * +"


def test_infix_to_postfix_division_and_multiplication():
    assert infix_to_postfix("a*b/c") == "a b * c /"


def test_infix_to_postfix_exponentiation_precedence():
    assert infix_to_postfix("a+b^c") == "a b c ^ +"


def test_infix_to_postfix_complex_with_all_operators():
    assert infix_to_postfix("a+b*c-d/e^f") == "a b c * + d e f ^ / -"