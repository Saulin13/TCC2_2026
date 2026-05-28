import pytest
from strings.wave_string import wave

def test_wave_normal_cases():
    assert wave('cat') == ['Cat', 'cAt', 'caT']
    assert wave('one') == ['One', 'oNe', 'onE']
    assert wave('book') == ['Book', 'bOok', 'boOk', 'booK']
    assert wave('hello') == ['Hello', 'hEllo', 'heLlo', 'helLo', 'hellO']

def test_wave_edge_cases():
    assert wave('') == []
    assert wave('a') == ['A']
    assert wave('ab') == ['Ab', 'aB']
    assert wave(' ') == []
    assert wave('  ') == []
    assert wave('a b') == ['A b', 'a B']

def test_wave_with_non_alpha_characters():
    assert wave('123') == []
    assert wave('1a2') == ['1A2']
    assert wave('a1b2') == ['A1b2', 'a1B2']
    assert wave('!@#') == []
    assert wave('a!b') == ['A!b', 'a!B']

def test_wave_failure_cases():
    with pytest.raises(TypeError):
        wave(None)
    with pytest.raises(TypeError):
        wave(123)
    with pytest.raises(TypeError):
        wave(['a', 'b', 'c'])