import sys
import os
sys.path.append(r'C:\Users\diogo\OneDrive\Área de Trabalho\Diogo\PUC\8 Periodo\TCC\TCC2_2026/repos/Python')
from computer_vision.haralick_descriptors import transform
import os
import sys




import numpy as np
import pytest

def test_transform_erosion():
    image = np.array([[1, 0.5], [0.2, 0.7]])
    binarized_image = np.array([[1, 1], [0, 1]], dtype=np.uint8)
    expected_output = np.array([[1, 1], [1, 1]], dtype=np.uint8)
    result = transform(binarized_image, 'erosion')
    np.testing.assert_array_equal(result, expected_output)

def test_transform_dilation():
    image = np.array([[1, 0.5], [0.2, 0.7]])
    binarized_image = np.array([[1, 1], [0, 1]], dtype=np.uint8)
    expected_output = np.array([[0, 0], [0, 0]], dtype=np.uint8)
    result = transform(binarized_image, 'dilation')
    np.testing.assert_array_equal(result, expected_output)

def test_transform_custom_kernel():
    image = np.array([[1, 0.5], [0.2, 0.7]])
    binarized_image = np.array([[1, 1], [0, 1]], dtype=np.uint8)
    kernel = np.array([[1, 0], [0, 1]])
    expected_output_erosion = np.array([[1, 1], [1, 1]], dtype=np.uint8)
    expected_output_dilation = np.array([[0, 0], [0, 0]], dtype=np.uint8)
    
    result_erosion = transform(binarized_image, 'erosion', kernel)
    result_dilation = transform(binarized_image, 'dilation', kernel)
    
    np.testing.assert_array_equal(result_erosion, expected_output_erosion)
    np.testing.assert_array_equal(result_dilation, expected_output_dilation)

def test_transform_invalid_kind():
    image = np.array([[1, 0.5], [0.2, 0.7]])
    binarized_image = np.array([[1, 1], [0, 1]], dtype=np.uint8)
    with pytest.raises(ValueError):
        transform(binarized_image, 'invalid_kind')

