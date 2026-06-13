import pytest
from strings.wave_string import wave


def test_wave_simple_word():
    assert wave('cat') == ['Cat', 'cAt', 'caT']


def test_wave_another_simple_word():
    assert wave('one') == ['One', 'oNe', 'onE']


def test_wave_four_letter_word():
    assert wave('book') == ['Book', 'bOok', 'boOk', 'booK']


def test_wave_single_character():
    assert wave('a') == ['A']


def test_wave_empty_string():
    assert wave('') == []


def test_wave_with_spaces():
    assert wave('a b') == ['A b', 'a B']


def test_wave_with_multiple_spaces():
    assert wave('hi there') == ['Hi there', 'hI there', 'hi There', 'hi tHere', 'hi thEre', 'hi theRe', 'hi therE']


def test_wave_with_numbers():
    assert wave('a1b') == ['A1b', 'a1B']


def test_wave_only_numbers():
    assert wave('123') == []


def test_wave_with_special_characters():
    assert wave('a!b') == ['A!b', 'a!B']


def test_wave_only_special_characters():
    assert wave('!@#') == []


def test_wave_mixed_case_input():
    assert wave('HeLLo') == ['HeLLo', 'hELLo', 'heLLo', 'helLo', 'hellO']


def test_wave_with_leading_space():
    assert wave(' cat') == [' Cat', ' cAt', ' caT']


def test_wave_with_trailing_space():
    assert wave('cat ') == ['Cat ', 'cAt ', 'caT ']


def test_wave_long_word():
    assert wave('python') == ['Python', 'pYthon', 'pyThon', 'pytHon', 'pythOn', 'pythoN']


def test_wave_with_tabs_and_newlines():
    assert wave('a\tb\nc') == ['A\tb\nc', 'a\tB\nc', 'a\tb\nC']


def test_wave_attribute_error_on_non_string():
    with pytest.raises(AttributeError):
        wave(None)


def test_wave_type_error_on_integer():
    with pytest.raises(TypeError):
        wave(123)


def test_wave_type_error_on_list():
    with pytest.raises(TypeError):
        wave(['a', 'b', 'c'])