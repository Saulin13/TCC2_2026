import sys
import os
sys.path.append(r'C:\Users\diogo\OneDrive\Área de Trabalho\Diogo\PUC\8 Periodo\TCC\TCC2_2026/repos/Python')
from conversions.rgb_cmyk_conversion import rgb_to_cmyk
import os
import sys




import pytest
  # substitua 'your_module' pelo nome do módulo onde a função está definida

def test_rgb_to_cmyk_white():
    assert rgb_to_cmyk(255, 255, 255) == (0, 0, 0, 0)

def test_rgb_to_cmyk_gray():
    assert rgb_to_cmyk(128, 128, 128) == (0, 0, 0, 50)

def test_rgb_to_cmyk_black():
    assert rgb_to_cmyk(0, 0, 0) == (0, 0, 0, 100)

def test_rgb_to_cmyk_red():
    assert rgb_to_cmyk(255, 0, 0) == (0, 100, 100, 0)

def test_rgb_to_cmyk_green():
    assert rgb_to_cmyk(0, 255, 0) == (100, 0, 100, 0)

def test_rgb_to_cmyk_blue():
    assert rgb_to_cmyk(0, 0, 255) == (100, 100, 0, 0)

def test_rgb_to_cmyk_invalid_type():
    with pytest.raises(ValueError, match=r"Expected int, found \(<class 'int'>, <class 'int'>, <class 'str'>\)"):
        rgb_to_cmyk(255, 200, "a")

def test_rgb_to_cmyk_out_of_range():
    with pytest.raises(ValueError, match="Expected int of the range 0..255"):
        rgb_to_cmyk(255, 255, 999)
