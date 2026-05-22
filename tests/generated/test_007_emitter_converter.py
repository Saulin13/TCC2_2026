import pytest
from hashes.hamming_code import emitter_converter

def test_emitter_converter_normal_case():
    assert emitter_converter(4, "101010111111") == ['1', '1', '1', '1', '0', '1', '0', '0', '1', '0', '1', '1', '1', '1', '1', '1']

def test_emitter_converter_edge_case_minimal_data():
    assert emitter_converter(2, "1") == ['1', '1', '1']

def test_emitter_converter_edge_case_no_parity():
    assert emitter_converter(0, "1010") == ['1', '0', '1', '0']

def test_emitter_converter_edge_case_large_parity():
    assert emitter_converter(5, "1") == ['1', '0', '0', '0', '0', '1']

def test_emitter_converter_exception_case():
    with pytest.raises(ValueError, match="size of parity don't match with size of data"):
        emitter_converter(5, "101010111111")