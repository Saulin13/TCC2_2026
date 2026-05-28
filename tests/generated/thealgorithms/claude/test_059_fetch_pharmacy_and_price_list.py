import pytest
from unittest.mock import Mock, patch
from web_programming.fetch_well_rx_price import fetch_pharmacy_and_price_list


@pytest.fixture
def mock_html_response():
    return """
    <html>
        <body>
            <div class="grid-x pharmCard">
                <p class="list-title">CVS Pharmacy</p>
                <span class="price price-large">$25.99</span>
            </div>
            <div class="grid-x pharmCard">
                <p class="list-title">Walgreens</p>
                <span class="price price-large">$27.50</span>
            </div>
            <div class="grid-x pharmCard">
                <p class="list-title">Walmart Pharmacy</p>
                <span class="price price-large">$22.00</span>
            </div>
        </body>
    </html>
    """


@pytest.fixture
def mock_empty_html_response():
    return """
    <html>
        <body>
        </body>
    </html>
    """


def test_fetch_pharmacy_and_price_list_success(mock_html_response):
    with patch('web_programming.fetch_well_rx_price.httpx.get') as mock_get:
        mock_response = Mock()
        mock_response.text = mock_html_response
        mock_response.raise_for_status.return_value = mock_response
        mock_get.return_value = mock_response
        
        result = fetch_pharmacy_and_price_list("eliquis", "30303")
        
        assert result is not None
        assert len(result) == 3
        assert result[0]["pharmacy_name"] == "CVS Pharmacy"
        assert result[0]["price"] == "$25.99"
        assert result[1]["pharmacy_name"] == "Walgreens"
        assert result[1]["price"] == "$27.50"
        assert result[2]["pharmacy_name"] == "Walmart Pharmacy"
        assert result[2]["price"] == "$22.00"


def test_fetch_pharmacy_and_price_list_empty_results(mock_empty_html_response):
    with patch('web_programming.fetch_well_rx_price.httpx.get') as mock_get:
        mock_response = Mock()
        mock_response.text = mock_empty_html_response
        mock_response.raise_for_status.return_value = mock_response
        mock_get.return_value = mock_response
        
        result = fetch_pharmacy_and_price_list("unknowndrug", "12345")
        
        assert result == []


def test_fetch_pharmacy_and_price_list_none_drug_name():
    result = fetch_pharmacy_and_price_list(None, "30303")
    assert result is None


def test_fetch_pharmacy_and_price_list_none_zip_code():
    result = fetch_pharmacy_and_price_list("eliquis", None)
    assert result is None


def test_fetch_pharmacy_and_price_list_both_none():
    result = fetch_pharmacy_and_price_list(None, None)
    assert result is None


def test_fetch_pharmacy_and_price_list_empty_drug_name():
    result = fetch_pharmacy_and_price_list("", "30303")
    assert result is None


def test_fetch_pharmacy_and_price_list_empty_zip_code():
    result = fetch_pharmacy_and_price_list("eliquis", "")
    assert result is None


def test_fetch_pharmacy_and_price_list_both_empty():
    result = fetch_pharmacy_and_price_list("", "")
    assert result is None


def test_fetch_pharmacy_and_price_list_http_error():
    with patch('web_programming.fetch_well_rx_price.httpx.get') as mock_get:
        mock_get.side_effect = Exception("HTTP Error")
        
        result = fetch_pharmacy_and_price_list("eliquis", "30303")
        
        assert result is None


def test_fetch_pharmacy_and_price_list_timeout():
    with patch('web_programming.fetch_well_rx_price.httpx.get') as mock_get:
        import httpx
        mock_get.side_effect = httpx.TimeoutException("Timeout")
        
        result = fetch_pharmacy_and_price_list("eliquis", "30303")
        
        assert result is None


def test_fetch_pharmacy_and_price_list_single_result():
    single_result_html = """
    <html>
        <body>
            <div class="grid-x pharmCard">
                <p class="list-title">Target Pharmacy</p>
                <span class="price price-large">$30.00</span>
            </div>
        </body>
    </html>
    """
    
    with patch('web_programming.fetch_well_rx_price.httpx.get') as mock_get:
        mock_response = Mock()
        mock_response.text = single_result_html
        mock_response.raise_for_status.return_value = mock_response
        mock_get.return_value = mock_response
        
        result = fetch_pharmacy_and_price_list("aspirin", "90210")
        
        assert result is not None
        assert len(result) == 1
        assert result[0]["pharmacy_name"] == "Target Pharmacy"
        assert result[0]["price"] == "$30.00"


def test_fetch_pharmacy_and_price_list_valid_inputs_with_spaces():
    with patch('web_programming.fetch_well_rx_price.httpx.get') as mock_get:
        mock_response = Mock()
        mock_response.text = """
        <html>
            <body>
                <div class="grid-x pharmCard">
                    <p class="list-title">Rite Aid</p>
                    <span class="price price-large">$15.75</span>
                </div>
            </body>
        </html>
        """
        mock_response.raise_for_status.return_value = mock_response
        mock_get.return_value = mock_response
        
        result = fetch_pharmacy_and_price_list("vitamin d", "10001")
        
        assert result is not None
        assert len(result) == 1
        assert result[0]["pharmacy_name"] == "Rite Aid"
        assert result[0]["price"] == "$15.75"