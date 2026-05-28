import pytest
from conversions.speed_conversions import convert_speed


def test_convert_kmh_to_ms():
    assert convert_speed(100, "km/h", "m/s") == 27.778


def test_convert_kmh_to_mph():
    assert convert_speed(100, "km/h", "mph") == 62.137


def test_convert_kmh_to_knot():
    assert convert_speed(100, "km/h", "knot") == 53.996


def test_convert_ms_to_kmh():
    assert convert_speed(100, "m/s", "km/h") == 360.0


def test_convert_ms_to_mph():
    assert convert_speed(100, "m/s", "mph") == 223.694


def test_convert_ms_to_knot():
    assert convert_speed(100, "m/s", "knot") == 194.384


def test_convert_mph_to_kmh():
    assert convert_speed(100, "mph", "km/h") == 160.934


def test_convert_mph_to_ms():
    assert convert_speed(100, "mph", "m/s") == 44.704


def test_convert_mph_to_knot():
    assert convert_speed(100, "mph", "knot") == 86.898


def test_convert_knot_to_kmh():
    assert convert_speed(100, "knot", "km/h") == 185.2


def test_convert_knot_to_ms():
    assert convert_speed(100, "knot", "m/s") == 51.444


def test_convert_knot_to_mph():
    assert convert_speed(100, "knot", "mph") == 115.078


def test_convert_same_unit_kmh():
    assert convert_speed(100, "km/h", "km/h") == 100.0


def test_convert_same_unit_ms():
    assert convert_speed(50, "m/s", "m/s") == 50.0


def test_convert_zero_speed():
    assert convert_speed(0, "km/h", "m/s") == 0.0


def test_convert_negative_speed():
    assert convert_speed(-50, "km/h", "m/s") == -13.889


def test_convert_decimal_speed():
    assert convert_speed(55.5, "mph", "km/h") == 89.319


def test_convert_small_speed():
    assert convert_speed(0.001, "km/h", "m/s") == 0.0


def test_convert_large_speed():
    assert convert_speed(10000, "km/h", "mph") == 6213.712


def test_invalid_unit_from():
    with pytest.raises(ValueError) as exc_info:
        convert_speed(100, "invalid_unit", "km/h")
    assert "Incorrect 'from_type' or 'to_type' value" in str(exc_info.value)
    assert "invalid_unit" in str(exc_info.value)


def test_invalid_unit_to():
    with pytest.raises(ValueError) as exc_info:
        convert_speed(100, "km/h", "invalid_unit")
    assert "Incorrect 'from_type' or 'to_type' value" in str(exc_info.value)
    assert "invalid_unit" in str(exc_info.value)


def test_invalid_both_units():
    with pytest.raises(ValueError) as exc_info:
        convert_speed(100, "invalid_from", "invalid_to")
    assert "Incorrect 'from_type' or 'to_type' value" in str(exc_info.value)


def test_case_sensitive_unit():
    with pytest.raises(ValueError) as exc_info:
        convert_speed(100, "KM/H", "m/s")
    assert "Incorrect 'from_type' or 'to_type' value" in str(exc_info.value)