import sys
import os
sys.path.append(r'C:\Users\diogo\OneDrive\Área de Trabalho\Diogo\PUC\8 Periodo\TCC\TCC2_2026/repos/Python')
from digital_image_processing.convert_to_negative import convert_to_negative
import os
import sys




import pytest
import numpy as np

def test_convert_to_negative():
    # Test case 1: Check conversion of a simple 2x2 image
    img = np.array([[[100, 150, 200], [50, 100, 150]],
                    [[200, 50, 100], [150, 200, 50]]], dtype=np.uint8)
    expected_output = np.array([[[155, 105, 55], [205, 155, 105]],
                                [[55, 205, 155], [105, 55, 205]]], dtype=np.uint8)
    assert np.array_equal(convert_to_negative(img), expected_output)

    # Test case 2: Check conversion of an image with all zeros (black)
    img = np.zeros((2, 2, 3), dtype=np.uint8)
    expected_output = np.array([[[255, 255, 255], [255, 255, 255]],
                                [[255, 255, 255], [255, 255, 255]]], dtype=np.uint8)
    assert np.array_equal(convert_to_negative(img), expected_output)

    # Test case 3: Check conversion of an image with all 255s (white)
    img = np.full((2, 2, 3), 255, dtype=np.uint8)
    expected_output = np.zeros((2, 2, 3), dtype=np.uint8)
    assert np.array_equal(convert_to_negative(img), expected_output)

    # Test case 4: Check conversion of a single pixel image
    img = np.array([[[123, 234, 56]]], dtype=np.uint8)
    expected_output = np.array([[[132, 21, 199]]], dtype=np.uint8)
    assert np.array_equal(convert_to_negative(img), expected_output)
