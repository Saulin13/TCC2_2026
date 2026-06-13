import pytest
from matrix.pascal_triangle import generate_pascal_triangle_optimized

def test_generate_pascal_triangle_optimized_normal_cases():
    assert generate_pascal_triangle_optimized(1) == [[1]]
    assert generate_pascal_triangle_optimized(2) == [[1], [1, 1]]
    assert generate_pascal_triangle_optimized(3) == [[1], [1, 1], [1, 2, 1]]
    assert generate_pascal_triangle_optimized(4) == [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1]]
    assert generate_pascal_triangle_optimized(5) == [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]

def test_generate_pascal_triangle_optimized_edge_cases():
    assert generate_pascal_triangle_optimized(0) == []
    assert generate_pascal_triangle_optimized(10) == [
        [1],
        [1, 1],
        [1, 2, 1],
        [1, 3, 3, 1],
        [1, 4, 6, 4, 1],
        [1, 5, 10, 10, 5, 1],
        [1, 6, 15, 20, 15, 6, 1],
        [1, 7, 21, 35, 35, 21, 7, 1],
        [1, 8, 28, 56, 70, 56, 28, 8, 1],
        [1, 9, 36, 84, 126, 126, 84, 36, 9, 1]
    ]

def test_generate_pascal_triangle_optimized_invalid_input():
    with pytest.raises(ValueError, match="The input value of 'num_rows' should be greater than or equal to 0"):
        generate_pascal_triangle_optimized(-1)

    with pytest.raises(TypeError, match="The input value of 'num_rows' should be 'int'"):
        generate_pascal_triangle_optimized(5.5)

    with pytest.raises(TypeError, match="The input value of 'num_rows' should be 'int'"):
        generate_pascal_triangle_optimized("3")