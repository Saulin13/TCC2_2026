import pytest
from web_programming.reddit import get_subreddit_data
from unittest.mock import patch, Mock
import httpx

# Mock valid_terms for testing purposes
valid_terms = {"title", "score", "id", "url"}

@pytest.fixture
def mock_response():
    return {
        "data": {
            "children": [
                {"data": {"title": "Post 1", "score": 100, "id": "abc123", "url": "http://example.com/1"}},
                {"data": {"title": "Post 2", "score": 150, "id": "def456", "url": "http://example.com/2"}},
            ]
        }
    }

@patch('web_programming.reddit.httpx.get')
def test_get_subreddit_data_normal_case(mock_get, mock_response):
    mock_get.return_value = Mock(status_code=200, json=lambda: mock_response)
    result = get_subreddit_data("python", limit=2, age="new", wanted_data=["title", "score"])
    expected = {
        0: {"title": "Post 1", "score": 100},
        1: {"title": "Post 2", "score": 150},
    }
    assert result == expected

@patch('web_programming.reddit.httpx.get')
def test_get_subreddit_data_no_wanted_data(mock_get, mock_response):
    mock_get.return_value = Mock(status_code=200, json=lambda: mock_response)
    result = get_subreddit_data("python", limit=2, age="new")
    expected = {
        0: mock_response["data"]["children"][0],
        1: mock_response["data"]["children"][1],
    }
    assert result == expected

@patch('web_programming.reddit.httpx.get')
def test_get_subreddit_data_invalid_wanted_data(mock_get):
    mock_get.return_value = Mock(status_code=200, json=lambda: {})
    with pytest.raises(ValueError, match="Invalid search term: invalid_term"):
        get_subreddit_data("python", limit=1, age="new", wanted_data=["invalid_term"])

@patch('web_programming.reddit.httpx.get')
def test_get_subreddit_data_http_error(mock_get):
    mock_get.return_value = Mock(status_code=429, raise_for_status=Mock(side_effect=httpx.HTTPError))
    with pytest.raises(httpx.HTTPError):
        get_subreddit_data("python", limit=1, age="new")

@patch('web_programming.reddit.httpx.get')
def test_get_subreddit_data_empty_subreddit(mock_get):
    mock_get.return_value = Mock(status_code=200, json=lambda: {"data": {"children": []}})
    result = get_subreddit_data("", limit=1, age="new")
    expected = {}
    assert result == expected