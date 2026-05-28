import pytest
from maths.numerical_analysis.newton_forward_interpolation import ucal

def test_ucal_normal_cases():
    assert ucal(1, 2) == 0
    assert ucal(1.1, 2) == pytest.approx(0.11000000000000011)
    assert ucal(1.2, 2) == pytest.approx(0.23999999999999994)
    assert ucal(2, 3) == 2
    assert ucal(2.5, 3) == pytest.approx(3.75)

def test_ucal_edge_cases():
    assert ucal(0, 1) == 0
    assert ucal(0, 0) == 0
    assert ucal(1, 1) == 1
    assert ucal(1, 0) == 1
    assert ucal(-1, 2) == 0

def test_ucal_failure_cases():
    with pytest.raises(TypeError):
        ucal('a', 2)
    with pytest.raises(TypeError):
        ucal(1, 'b')
    with pytest.raises(TypeError):
        ucal(None, 2)
    with pytest.raises(TypeError):
        ucal(1, None)