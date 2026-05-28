import pytest
from conversions.speed_conversions import convert_speed

def test_convert_speed_kmh_to_ms():
    assert convert_speed(100, "km/h", "m/s") == 27.778

def test_convert_speed_kmh_to_mph():
    assert convert_speed(100, "km/h", "mph") == 62.137

def test_convert_speed_kmh_to_knot():
    assert convert_speed(100, "km/h", "knot") == 53.996

def test_convert_speed_ms_to_kmh():
    assert convert_speed(100, "m/s", "km/h") == 360.0

def test_convert_speed_ms_to_mph():
    assert convert_speed(100, "m/s", "mph") == 223.694

def test_convert_speed_ms_to_knot():
    assert convert_speed(100, "m/s", "knot") == 194.384

def test_convert_speed_mph_to_kmh():
    assert convert_speed(100, "mph", "km/h") == 160.934

def test_convert_speed_mph_to_ms():
    assert convert_speed(100, "mph", "m/s") == 44.704

def test_convert_speed_mph_to_knot():
    assert convert_speed(100, "mph", "knot") == 86.898

def test_convert_speed_knot_to_kmh():
    assert convert_speed(100, "knot", "km/h") == 185.2

def test_convert_speed_knot_to_ms():
    assert convert_speed(100, "knot", "m/s") == 51.444

def test_convert_speed_knot_to_mph():
    assert convert_speed(100, "knot", "mph") == 115.078

def test_convert_speed_invalid_unit_from():
    with pytest.raises(ValueError, match="Incorrect 'from_type' or 'to_type' value"):
        convert_speed(100, "invalid", "km/h")

def test_convert_speed_invalid_unit_to():
    with pytest.raises(ValueError, match="Incorrect 'from_type' or 'to_type' value"):
        convert_speed(100, "km/h", "invalid")

def test_convert_speed_same_unit():
    assert convert_speed(100, "km/h", "km/h") == 100.0