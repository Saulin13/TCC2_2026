import pytest
from electronics.carrier_concentration import carrier_concentration


def test_calculate_intrinsic_concentration():
    result = carrier_concentration(electron_conc=25, hole_conc=100, intrinsic_conc=0)
    assert result[0] == "intrinsic_conc"
    assert result[1] == 50.0


def test_calculate_electron_concentration():
    result = carrier_concentration(electron_conc=0, hole_conc=1600, intrinsic_conc=200)
    assert result[0] == "electron_conc"
    assert result[1] == 25.0


def test_calculate_hole_concentration():
    result = carrier_concentration(electron_conc=1000, hole_conc=0, intrinsic_conc=1200)
    assert result[0] == "hole_conc"
    assert result[1] == 1440.0


def test_intrinsic_concentration_with_equal_carriers():
    result = carrier_concentration(electron_conc=100, hole_conc=100, intrinsic_conc=0)
    assert result[0] == "intrinsic_conc"
    assert result[1] == 100.0


def test_electron_concentration_with_small_values():
    result = carrier_concentration(electron_conc=0, hole_conc=0.5, intrinsic_conc=10)
    assert result[0] == "electron_conc"
    assert result[1] == 200.0


def test_hole_concentration_with_small_values():
    result = carrier_concentration(electron_conc=0.25, hole_conc=0, intrinsic_conc=5)
    assert result[0] == "hole_conc"
    assert result[1] == 100.0


def test_intrinsic_concentration_with_large_values():
    result = carrier_concentration(electron_conc=1e6, hole_conc=1e6, intrinsic_conc=0)
    assert result[0] == "intrinsic_conc"
    assert result[1] == 1e6


def test_electron_concentration_with_large_intrinsic():
    result = carrier_concentration(electron_conc=0, hole_conc=1e5, intrinsic_conc=1e7)
    assert result[0] == "electron_conc"
    assert result[1] == 1e9


def test_all_three_values_supplied():
    with pytest.raises(ValueError, match="You cannot supply more or less than 2 values"):
        carrier_concentration(electron_conc=1000, hole_conc=400, intrinsic_conc=1200)


def test_no_zero_values_supplied():
    with pytest.raises(ValueError, match="You cannot supply more or less than 2 values"):
        carrier_concentration(electron_conc=1000, hole_conc=400, intrinsic_conc=600)


def test_all_zero_values():
    with pytest.raises(ValueError, match="You cannot supply more or less than 2 values"):
        carrier_concentration(electron_conc=0, hole_conc=0, intrinsic_conc=0)


def test_two_zero_values():
    with pytest.raises(ValueError, match="You cannot supply more or less than 2 values"):
        carrier_concentration(electron_conc=0, hole_conc=0, intrinsic_conc=100)


def test_negative_electron_concentration():
    with pytest.raises(ValueError, match="Electron concentration cannot be negative in a semiconductor"):
        carrier_concentration(electron_conc=-1000, hole_conc=0, intrinsic_conc=1200)


def test_negative_hole_concentration():
    with pytest.raises(ValueError, match="Hole concentration cannot be negative in a semiconductor"):
        carrier_concentration(electron_conc=0, hole_conc=-400, intrinsic_conc=1200)


def test_negative_intrinsic_concentration():
    with pytest.raises(ValueError, match="Intrinsic concentration cannot be negative in a semiconductor"):
        carrier_concentration(electron_conc=0, hole_conc=400, intrinsic_conc=-1200)


def test_negative_electron_with_all_values():
    with pytest.raises(ValueError, match="Electron concentration cannot be negative in a semiconductor"):
        carrier_concentration(electron_conc=-100, hole_conc=400, intrinsic_conc=1200)


def test_negative_hole_with_zero_electron():
    with pytest.raises(ValueError, match="Hole concentration cannot be negative in a semiconductor"):
        carrier_concentration(electron_conc=0, hole_conc=-100, intrinsic_conc=500)


def test_negative_intrinsic_with_zero_hole():
    with pytest.raises(ValueError, match="Intrinsic concentration cannot be negative in a semiconductor"):
        carrier_concentration(electron_conc=100, hole_conc=0, intrinsic_conc=-500)