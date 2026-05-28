import pytest
from electronics.carrier_concentration import carrier_concentration

def test_calculate_intrinsic_concentration():
    assert carrier_concentration(electron_conc=25, hole_conc=100, intrinsic_conc=0) == ('intrinsic_conc', 50.0)

def test_calculate_electron_concentration():
    assert carrier_concentration(electron_conc=0, hole_conc=1600, intrinsic_conc=200) == ('electron_conc', 25.0)

def test_calculate_hole_concentration():
    assert carrier_concentration(electron_conc=1000, hole_conc=0, intrinsic_conc=1200) == ('hole_conc', 1440.0)

def test_more_than_two_non_zero_values():
    with pytest.raises(ValueError, match="You cannot supply more or less than 2 values"):
        carrier_concentration(electron_conc=1000, hole_conc=400, intrinsic_conc=1200)

def test_negative_electron_concentration():
    with pytest.raises(ValueError, match="Electron concentration cannot be negative in a semiconductor"):
        carrier_concentration(electron_conc=-1000, hole_conc=0, intrinsic_conc=1200)

def test_negative_hole_concentration():
    with pytest.raises(ValueError, match="Hole concentration cannot be negative in a semiconductor"):
        carrier_concentration(electron_conc=0, hole_conc=-400, intrinsic_conc=1200)

def test_negative_intrinsic_concentration():
    with pytest.raises(ValueError, match="Intrinsic concentration cannot be negative in a semiconductor"):
        carrier_concentration(electron_conc=0, hole_conc=400, intrinsic_conc=-1200)

def test_all_zero_values():
    with pytest.raises(ValueError, match="You cannot supply more or less than 2 values"):
        carrier_concentration(electron_conc=0, hole_conc=0, intrinsic_conc=0)