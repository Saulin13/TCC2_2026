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


def test_intrinsic_concentration_with_equal_values():
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
    result = carrier_concentration(electron_conc=10000, hole_conc=10000, intrinsic_conc=0)
    assert result[0] == "intrinsic_conc"
    assert result[1] == 10000.0


def test_electron_concentration_with_large_values():
    result = carrier_concentration(electron_conc=0, hole_conc=1000000, intrinsic_conc=10000)
    assert result[0] == "electron_conc"
    assert result[1] == 100.0


def test_all_three_values_supplied():
    with pytest.raises(ValueError, match="You cannot supply more or less than 2 values"):
        carrier_concentration(electron_conc=1000, hole_conc=400, intrinsic_conc=1200)


def test_no_zero_values_supplied():
    with pytest.raises(ValueError, match="You cannot supply more or less than 2 values"):
        carrier_concentration(electron_conc=1000, hole_conc=400, intrinsic_conc=1200)


def test_two_zero_values_supplied():
    with pytest.raises(ValueError, match="You cannot supply more or less than 2 values"):
        carrier_concentration(electron_conc=0, hole_conc=0, intrinsic_conc=1200)


def test_all_zero_values_supplied():
    with pytest.raises(ValueError, match="You cannot supply more or less than 2 values"):
        carrier_concentration(electron_conc=0, hole_conc=0, intrinsic_conc=0)


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
        carrier_concentration(electron_conc=100, hole_conc=-400, intrinsic_conc=0)


def test_fractional_values():
    result = carrier_concentration(electron_conc=2.5, hole_conc=10.0, intrinsic_conc=0)
    assert result[0] == "intrinsic_conc"
    assert result[1] == pytest.approx(5.0, rel=1e-9)


def test_very_small_concentrations():
    result = carrier_concentration(electron_conc=0, hole_conc=0.001, intrinsic_conc=0.1)
    assert result[0] == "electron_conc"
    assert result[1] == pytest.approx(10.0, rel=1e-9)