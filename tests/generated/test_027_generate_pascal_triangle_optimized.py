import pytest
from matrix.pascal_triangle import generate_pascal_triangle_optimized

def test_generate_pascal_triangle_optimized_normal_case():
    assert generate_pascal_triangle_optimized(3) == [[1], [1, 1], [1, 2, 1]]
    assert generate_pascal_triangle_optimized(5) == [
        [1],
        [1, 1],
        [1, 2, 1],
        [1, 3, 3, 1],
        [1, 4, 6, 4, 1]
    ]

def test_generate_pascal_triangle_optimized_edge_case():
    assert generate_pascal_triangle_optimized(0) == []
    assert generate_pascal_triangle_optimized(1) == [[1]]

def test_generate_pascal_triangle_optimized_large_input():
    result = generate_pascal_triangle_optimized(10)
    assert len(result) == 10
    assert result[9] == [1, 9, 36, 84, 126, 126, 84, 36, 9, 1]

def test_generate_pascal_triangle_optimized_negative_input():
    with pytest.raises(ValueError, match="The input value of 'num_rows' should be greater than or equal to 0"):
        generate_pascal_triangle_optimized(-5)

def test_generate_pascal_triangle_optimized_non_integer_input():
    with pytest.raises(TypeError, match="The input value of 'num_rows' should be 'int'"):
        generate_pascal_triangle_optimized(7.89)
    with pytest.raises(TypeError, match="The input value of 'num_rows' should be 'int'"):
        generate_pascal_triangle_optimized("3")