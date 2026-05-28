import pytest
from unittest.mock import patch, Mock
from web_programming.fetch_well_rx_price import fetch_pharmacy_and_price_list

def test_fetch_pharmacy_and_price_list_valid_input():
    mock_html = """
    <div class="grid-x pharmCard">
        <p class="list-title">Pharmacy A</p>
        <span class="price price-large">$10.00</span>
    </div>
    <div class="grid-x pharmCard">
        <p class="list-title">Pharmacy B</p>
        <span class="price price-large">$12.00</span>
    </div>
    """
    with patch('httpx.get') as mock_get:
        mock_response = Mock()
        mock_response.text = mock_html
        mock_get.return_value = mock_response

        result = fetch_pharmacy_and_price_list("aspirin", "12345")
        expected = [
            {"pharmacy_name": "Pharmacy A", "price": "$10.00"},
            {"pharmacy_name": "Pharmacy B", "price": "$12.00"}
        ]
        assert result == expected

def test_fetch_pharmacy_and_price_list_no_drug_name():
    result = fetch_pharmacy_and_price_list(None, "12345")
    assert result is None

def test_fetch_pharmacy_and_price_list_no_zip_code():
    result = fetch_pharmacy_and_price_list("aspirin", None)
    assert result is None

def test_fetch_pharmacy_and_price_list_no_inputs():
    result = fetch_pharmacy_and_price_list(None, None)
    assert result is None

def test_fetch_pharmacy_and_price_list_empty_result():
    mock_html = ""
    with patch('httpx.get') as mock_get:
        mock_response = Mock()
        mock_response.text = mock_html
        mock_get.return_value = mock_response

        result = fetch_pharmacy_and_price_list("aspirin", "12345")
        assert result == []

def test_fetch_pharmacy_and_price_list_http_error():
    with patch('httpx.get', side_effect=Exception("HTTP Error")):
        result = fetch_pharmacy_and_price_list("aspirin", "12345")
        assert result is None