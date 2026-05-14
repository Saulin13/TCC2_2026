import sys
import os
sys.path.append(r'C:\Users\diogo\OneDrive\Área de Trabalho\Diogo\PUC\8 Periodo\TCC\TCC2_2026/repos/Python')
from conversions.rgb_hsv_conversion import rgb_to_hsv
import os
import sys




import pytest

def approximately_equal_hsv(hsv1, hsv2, tolerance=1e-2):
    return all(abs(a - b) < tolerance for a, b in zip(hsv1, hsv2))

def test_rgb_to_hsv():
    assert approximately_equal_hsv(rgb_to_hsv(0, 0, 0), [0, 0, 0])
    assert approximately_equal_hsv(rgb_to_hsv(255, 255, 255), [0, 0, 1])
    assert approximately_equal_hsv(rgb_to_hsv(255, 0, 0), [0, 1, 1])
    assert approximately_equal_hsv(rgb_to_hsv(255, 255, 0), [60, 1, 1])
    assert approximately_equal_hsv(rgb_to_hsv(0, 255, 0), [120, 1, 1])
    assert approximately_equal_hsv(rgb_to_hsv(0, 0, 255), [240, 1, 1])
    assert approximately_equal_hsv(rgb_to_hsv(255, 0, 255), [300, 1, 1])
    assert approximately_equal_hsv(rgb_to_hsv(64, 128, 128), [180, 0.5, 0.5])
    assert approximately_equal_hsv(rgb_to_hsv(193, 196, 224), [234, 0.14, 0.88])
    assert approximately_equal_hsv(rgb_to_hsv(128, 32, 80), [330, 0.75, 0.5])

    with pytest.raises(Exception, match="red should be between 0 and 255"):
        rgb_to_hsv(-1, 0, 0)
    with pytest.raises(Exception, match="green should be between 0 and 255"):
        rgb_to_hsv(0, -1, 0)
    with pytest.raises(Exception, match="blue should be between 0 and 255"):
        rgb_to_hsv(0, 0, -1)
    with pytest.raises(Exception, match="red should be between 0 and 255"):
        rgb_to_hsv(256, 0, 0)
    with pytest.raises(Exception, match="green should be between 0 and 255"):
        rgb_to_hsv(0, 256, 0)
    with pytest.raises(Exception, match="blue should be between 0 and 255"):
        rgb_to_hsv(0, 0, 256)
