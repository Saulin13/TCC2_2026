import pytest
from strings.wave_string import wave

def test_wave_normal_cases():
    assert wave('cat') == ['Cat', 'cAt', 'caT']
    assert wave('one') == ['One', 'oNe', 'onE']
    assert wave('book') == ['Book', 'bOok', 'boOk', 'booK']
    assert wave('hello') == ['Hello', 'hEllo', 'heLlo', 'helLo', 'hellO']

def test_wave_with_spaces():
    assert wave('a b') == ['A b', 'a B']
    assert wave('ab cd') == ['Ab cd', 'aB cd', 'ab Cd', 'ab cD']

def test_wave_empty_string():
    assert wave('') == []

def test_wave_all_spaces():
    assert wave('   ') == []

def test_wave_with_numbers_and_punctuation():
    assert wave('a1b!') == ['A1b!', 'a1B!']
    assert wave('123!') == []

def test_wave_single_character():
    assert wave('a') == ['A']
    assert wave('z') == ['Z']

def test_wave_no_alphabetic_characters():
    assert wave('123') == []
    assert wave('!@#') == []

def test_wave_failure_path():
    with pytest.raises(TypeError):
        wave(None)