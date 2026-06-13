import pytest
from data_structures.stacks.infix_to_postfix_conversion import infix_to_postfix

def test_infix_to_postfix_basic_operations():
    assert infix_to_postfix("3+2") == "3 2 +"
    assert infix_to_postfix("(3+4)*5-6") == "3 4 + 5 * 6 -"
    assert infix_to_postfix("(1+2)*3/4-5") == "1 2 + 3 * 4 / 5 -"

def test_infix_to_postfix_with_variables():
    assert infix_to_postfix("a+b*c+(d*e+f)*g") == "a b c * + d e * f + g * +"
    assert infix_to_postfix("x^y/(5*z)+2") == "x y ^ 5 z * / 2 +"

def test_infix_to_postfix_exponentiation():
    assert infix_to_postfix("2^3^2") == "2 3 2 ^ ^"

def test_infix_to_postfix_empty_string():
    assert infix_to_postfix("") == ""

def test_infix_to_postfix_mismatched_parentheses():
    with pytest.raises(ValueError, match="Mismatched parentheses"):
        infix_to_postfix("(1*(2+3)+4))")

def test_infix_to_postfix_single_operand():
    assert infix_to_postfix("42") == "42"

def test_infix_to_postfix_no_operators():
    assert infix_to_postfix("abc") == "a b c"

def test_infix_to_postfix_only_parentheses():
    with pytest.raises(ValueError, match="Mismatched parentheses"):
        infix_to_postfix("()")

def test_infix_to_postfix_complex_expression():
    assert infix_to_postfix("((a+b)*c-(d-e))^(f+g*h)-i") == "a b + c * d e - - f g h * + ^ i -"