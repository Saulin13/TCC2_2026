import sys
import os
sys.path.append(r'C:\Users\diogo\OneDrive\Área de Trabalho\Diogo\PUC\8 Periodo\TCC\TCC2_2026/repos/Python')
from digital_image_processing.edge_detection.canny import suppress_non_maximum
import os
import sys




import numpy as np
import pytest

def test_suppress_non_maximum():
    # Constants
    PI = np.pi

    # Test data
    image_shape = (5, 5)
    gradient_direction = np.array([
        [0, 0, 0, 0, 0],
        [0, PI/4, PI/4, PI/4, 0],
        [0, PI/2, PI/2, PI/2, 0],
        [0, 3*PI/4, 3*PI/4, 3*PI/4, 0],
        [0, 0, 0, 0, 0]
    ])
    sobel_grad = np.array([
        [0, 0, 0, 0, 0],
        [0, 10, 20, 10, 0],
        [0, 20, 30, 20, 0],
        [0, 10, 20, 10, 0],
        [0, 0, 0, 0, 0]
    ])
    expected_output = np.array([
        [0, 0, 0, 0, 0],
        [0, 0, 20, 0, 0],
        [0, 0, 30, 0, 0],
        [0, 0, 20, 0, 0],
        [0, 0, 0, 0, 0]
    ])

    # Run the function
    output = suppress_non_maximum(image_shape, gradient_direction, sobel_grad)

    # Assert the output
    np.testing.assert_array_equal(output, expected_output)

# Run the test
pytest.main([__file__])
