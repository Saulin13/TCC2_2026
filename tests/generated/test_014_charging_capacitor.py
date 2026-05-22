import pytest
from electronics.charging_capacitor import charging_capacitor

def test_charging_capacitor_normal_cases():
    assert charging_capacitor(0.2, 0.9, 8.4, 0.5) == 0.013
    assert charging_capacitor(2.2, 3.5, 2.4, 9) == 1.446
    assert charging_capacitor(15, 200, 20, 2) == 0.007
    assert charging_capacitor(20, 2000, 30*pow(10, -5), 4) == 19.975

def test_charging_capacitor_edge_cases():
    assert charging_capacitor(5, 1000, 0.0001, 0) == 0.0
    assert charging_capacitor(5, 1000, 0.0001, 1000) == 5.0

def test_charging_capacitor_invalid_source_voltage():
    with pytest.raises(ValueError, match="Source voltage must be positive."):
        charging_capacitor(0, 10.0, 0.30, 3)

def test_charging_capacitor_invalid_resistance():
    with pytest.raises(ValueError, match="Resistance must be positive."):
        charging_capacitor(20, -2000, 30, 4)

def test_charging_capacitor_invalid_capacitance():
    with pytest.raises(ValueError, match="Capacitance must be positive."):
        charging_capacitor(30, 1500, 0, 4)