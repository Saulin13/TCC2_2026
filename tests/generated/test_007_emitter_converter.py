import pytest
from hashes.hamming_code import emitter_converter

def test_emitter_converter_normal_case():
    result = emitter_converter(4, "101010111111")
    expected = ['1', '1', '1', '1', '0', '1', '0', '0', '1', '0', '1', '1', '1', '1', '1', '1']
    assert result == expected

def test_emitter_converter_edge_case_minimum_data():
    result = emitter_converter(3, "1")
    expected = ['1', '1', '1', '1']
    assert result == expected

def test_emitter_converter_edge_case_no_parity():
    result = emitter_converter(0, "101010")
    expected = ['1', '0', '1', '0', '1', '0']
    assert result == expected

def test_emitter_converter_exception_case():
    with pytest.raises(ValueError, match="size of parity don't match with size of data"):
        emitter_converter(5, "101010111111")

def test_emitter_converter_large_data():
    data = "101010101010101010101010101010"
    result = emitter_converter(5, data)
    expected_length = len(data) + 5
    assert len(result) == expected_length
    assert all(bit in ['0', '1'] for bit in result)