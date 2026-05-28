import pytest
from machine_learning.linear_discriminant_analysis import calculate_probabilities


def test_calculate_probabilities_normal_case_1():
    result = calculate_probabilities(20, 60)
    assert result == pytest.approx(0.3333333333333333)


def test_calculate_probabilities_normal_case_2():
    result = calculate_probabilities(30, 100)
    assert result == pytest.approx(0.3)


def test_calculate_probabilities_normal_case_3():
    result = calculate_probabilities(50, 200)
    assert result == pytest.approx(0.25)


def test_calculate_probabilities_normal_case_4():
    result = calculate_probabilities(1, 10)
    assert result == pytest.approx(0.1)


def test_calculate_probabilities_equal_counts():
    result = calculate_probabilities(100, 100)
    assert result == pytest.approx(1.0)


def test_calculate_probabilities_single_instance():
    result = calculate_probabilities(1, 1)
    assert result == pytest.approx(1.0)


def test_calculate_probabilities_zero_instances():
    result = calculate_probabilities(0, 100)
    assert result == pytest.approx(0.0)


def test_calculate_probabilities_large_numbers():
    result = calculate_probabilities(1000000, 10000000)
    assert result == pytest.approx(0.1)


def test_calculate_probabilities_small_fraction():
    result = calculate_probabilities(1, 1000)
    assert result == pytest.approx(0.001)


def test_calculate_probabilities_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        calculate_probabilities(10, 0)


def test_calculate_probabilities_negative_instance_count():
    result = calculate_probabilities(-10, 100)
    assert result == pytest.approx(-0.1)


def test_calculate_probabilities_negative_total_count():
    result = calculate_probabilities(10, -100)
    assert result == pytest.approx(-0.1)


def test_calculate_probabilities_both_negative():
    result = calculate_probabilities(-10, -100)
    assert result == pytest.approx(0.1)