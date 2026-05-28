import pytest
from matrix.pascal_triangle import generate_pascal_triangle_optimized


def test_generate_pascal_triangle_optimized_zero_rows():
    assert generate_pascal_triangle_optimized(0) == []


def test_generate_pascal_triangle_optimized_one_row():
    assert generate_pascal_triangle_optimized(1) == [[1]]


def test_generate_pascal_triangle_optimized_two_rows():
    assert generate_pascal_triangle_optimized(2) == [[1], [1, 1]]


def test_generate_pascal_triangle_optimized_three_rows():
    assert generate_pascal_triangle_optimized(3) == [[1], [1, 1], [1, 2, 1]]


def test_generate_pascal_triangle_optimized_four_rows():
    assert generate_pascal_triangle_optimized(4) == [
        [1],
        [1, 1],
        [1, 2, 1],
        [1, 3, 3, 1]
    ]


def test_generate_pascal_triangle_optimized_five_rows():
    assert generate_pascal_triangle_optimized(5) == [
        [1],
        [1, 1],
        [1, 2, 1],
        [1, 3, 3, 1],
        [1, 4, 6, 4, 1]
    ]


def test_generate_pascal_triangle_optimized_six_rows():
    assert generate_pascal_triangle_optimized(6) == [
        [1],
        [1, 1],
        [1, 2, 1],
        [1, 3, 3, 1],
        [1, 4, 6, 4, 1],
        [1, 5, 10, 10, 5, 1]
    ]


def test_generate_pascal_triangle_optimized_seven_rows():
    assert generate_pascal_triangle_optimized(7) == [
        [1],
        [1, 1],
        [1, 2, 1],
        [1, 3, 3, 1],
        [1, 4, 6, 4, 1],
        [1, 5, 10, 10, 5, 1],
        [1, 6, 15, 20, 15, 6, 1]
    ]


def test_generate_pascal_triangle_optimized_ten_rows():
    result = generate_pascal_triangle_optimized(10)
    assert len(result) == 10
    assert result[0] == [1]
    assert result[9] == [1, 9, 36, 84, 126, 126, 84, 36, 9, 1]


def test_generate_pascal_triangle_optimized_negative_value():
    with pytest.raises(ValueError) as exc_info:
        generate_pascal_triangle_optimized(-1)
    assert "The input value of 'num_rows' should be greater than or equal to 0" in str(exc_info.value)


def test_generate_pascal_triangle_optimized_negative_five():
    with pytest.raises(ValueError) as exc_info:
        generate_pascal_triangle_optimized(-5)
    assert "The input value of 'num_rows' should be greater than or equal to 0" in str(exc_info.value)


def test_generate_pascal_triangle_optimized_float_input():
    with pytest.raises(TypeError) as exc_info:
        generate_pascal_triangle_optimized(7.89)
    assert "The input value of 'num_rows' should be 'int'" in str(exc_info.value)


def test_generate_pascal_triangle_optimized_string_input():
    with pytest.raises(TypeError) as exc_info:
        generate_pascal_triangle_optimized("5")
    assert "The input value of 'num_rows' should be 'int'" in str(exc_info.value)


def test_generate_pascal_triangle_optimized_none_input():
    with pytest.raises(TypeError) as exc_info:
        generate_pascal_triangle_optimized(None)
    assert "The input value of 'num_rows' should be 'int'" in str(exc_info.value)


def test_generate_pascal_triangle_optimized_list_input():
    with pytest.raises(TypeError) as exc_info:
        generate_pascal_triangle_optimized([5])
    assert "The input value of 'num_rows' should be 'int'" in str(exc_info.value)