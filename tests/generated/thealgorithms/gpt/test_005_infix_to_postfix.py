import pytest
from data_structures.stacks.infix_to_postfix_conversion import infix_to_postfix

def test_infix_to_postfix_normal_cases():
    assert infix_to_postfix("3+2") == "3 2 +"
    assert infix_to_postfix("(3+4)*5-6") == "3 4 + 5 * 6 -"
    assert infix_to_postfix("(1+2)*3/4-5") == "1 2 + 3 * 4 / 5 -"
    assert infix_to_postfix("a+b*c+(d*e+f)*g") == "a b c * + d e * f + g * +"
    assert infix_to_postfix("x^y/(5*z)+2") == "x y ^ 5 z * / 2 +"
    assert infix_to_postfix("2^3^2") == "2 3 2 ^ ^"

def test_infix_to_postfix_edge_cases():
    assert infix_to_postfix("") == ""
    assert infix_to_postfix("a") == "a"
    assert infix_to_postfix("1") == "1"

def test_infix_to_postfix_mismatched_parentheses():
    with pytest.raises(ValueError, match="Mismatched parentheses"):
        infix_to_postfix("(1*(2+3)+4))")
    with pytest.raises(ValueError, match="Mismatched parentheses"):
        infix_to_postfix("((3+2)")
    with pytest.raises(ValueError, match="Mismatched parentheses"):
        infix_to_postfix(")(")