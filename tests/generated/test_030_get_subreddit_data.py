import pytest
from web_programming.reddit import get_subreddit_data
import httpx
from unittest.mock import patch

# Mock valid terms for testing
valid_terms = {"title", "author", "score", "url"}

# Mock response data
mock_data = {
    "data": {
        "children": [
            {"data": {"title": "Post 1", "author": "Author 1", "score": 100, "url": "http://example.com/1"}},
            {"data": {"title": "Post 2", "author": "Author 2", "score": 200, "url": "http://example.com/2"}},
        ]
    }
}

def mock_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        def raise_for_status(self):
            if self.status_code != 200:
                raise httpx.HTTPStatusError("Error", request=None, response=self)

    if "limit=1" in args[0]:
        return MockResponse({"data": {"children": [mock_data["data"]["children"][0]]}}, 200)
    elif "limit=2" in args[0]:
        return MockResponse(mock_data, 200)
    elif "limit=0" in args[0]:
        return MockResponse({"data": {"children": []}}, 200)
    return MockResponse(None, 404)

@patch('httpx.get', side_effect=mock_get)
def test_get_subreddit_data_basic(mock_get):
    result = get_subreddit_data("testsubreddit", limit=1)
    assert result == {0: mock_data["data"]["children"][0]}

@patch('httpx.get', side_effect=mock_get)
def test_get_subreddit_data_multiple_posts(mock_get):
    result = get_subreddit_data("testsubreddit", limit=2)
    assert result == {0: mock_data["data"]["children"][0], 1: mock_data["data"]["children"][1]}

@patch('httpx.get', side_effect=mock_get)
def test_get_subreddit_data_no_posts(mock_get):
    result = get_subreddit_data("testsubreddit", limit=0)
    assert result == {}

@patch('httpx.get', side_effect=mock_get)
def test_get_subreddit_data_wanted_data(mock_get):
    result = get_subreddit_data("testsubreddit", limit=1, wanted_data=["title", "author"])
    expected = {0: {"title": "Post 1", "author": "Author 1"}}
    assert result == expected

@patch('httpx.get', side_effect=mock_get)
def test_get_subreddit_data_invalid_wanted_data(mock_get):
    with pytest.raises(ValueError, match="Invalid search term: invalid_term"):
        get_subreddit_data("testsubreddit", limit=1, wanted_data=["invalid_term"])

@patch('httpx.get', side_effect=mock_get)
def test_get_subreddit_data_http_error(mock_get):
    with pytest.raises(httpx.HTTPStatusError):
        get_subreddit_data("testsubreddit", limit=1, age="invalid_age")