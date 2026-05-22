import pytest
from conversions.rgb_hsv_conversion import approximately_equal_hsv

def test_approximately_equal_hsv_identical():
    assert approximately_equal_hsv([0, 0, 0], [0, 0, 0]) == True

def test_approximately_equal_hsv_close_values():
    assert approximately_equal_hsv([180, 0.5, 0.3], [179.9999, 0.500001, 0.30001]) == True

def test_approximately_equal_hsv_different_hue():
    assert approximately_equal_hsv([0, 0, 0], [1, 0, 0]) == False

def test_approximately_equal_hsv_different_saturation():
    assert approximately_equal_hsv([180, 0.5, 0.3], [179.9999, 0.6, 0.30001]) == False

def test_approximately_equal_hsv_edge_case_hue():
    assert approximately_equal_hsv([0.1, 0.5, 0.5], [0.3, 0.5, 0.5]) == False

def test_approximately_equal_hsv_edge_case_saturation():
    assert approximately_equal_hsv([180, 0.5, 0.5], [180, 0.502, 0.5]) == False

def test_approximately_equal_hsv_edge_case_value():
    assert approximately_equal_hsv([180, 0.5, 0.5], [180, 0.5, 0.502]) == False

def test_approximately_equal_hsv_invalid_input_length():
    with pytest.raises(IndexError):
        approximately_equal_hsv([180, 0.5], [180, 0.5, 0.5])

def test_approximately_equal_hsv_invalid_input_type():
    with pytest.raises(TypeError):
        approximately_equal_hsv("180, 0.5, 0.5", [180, 0.5, 0.5])