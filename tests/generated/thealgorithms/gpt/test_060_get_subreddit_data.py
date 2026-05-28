import pytest
from web_programming.reddit import get_subreddit_data
import httpx
from unittest.mock import patch

# Mock response data
mock_data = {
    "data": {
        "children": [
            {"data": {"title": "Post 1", "score": 100}},
            {"data": {"title": "Post 2", "score": 150}},
        ]
    }
}

valid_terms = {"title", "score", "author", "created_utc"}

# Test normal case
def test_get_subreddit_data_normal():
    with patch('httpx.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_data

        result = get_subreddit_data("python", limit=2, age="new", wanted_data=["title", "score"])
        expected = {
            0: {"title": "Post 1", "score": 100},
            1: {"title": "Post 2", "score": 150}
        }
        assert result == expected

# Test edge case with empty wanted_data
def test_get_subreddit_data_empty_wanted_data():
    with patch('httpx.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_data

        result = get_subreddit_data("python", limit=1, age="new", wanted_data=[])
        expected = {0: {"title": "Post 1", "score": 100}}
        assert result == expected

# Test edge case with limit = 0
def test_get_subreddit_data_zero_limit():
    with patch('httpx.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_data

        result = get_subreddit_data("python", limit=0, age="new", wanted_data=["title"])
        expected = {}
        assert result == expected

# Test invalid search term
def test_get_subreddit_data_invalid_search_term():
    with pytest.raises(ValueError, match="Invalid search term: invalid_term"):
        get_subreddit_data("python", limit=1, age="new", wanted_data=["invalid_term"])

# Test HTTP 429 error
def test_get_subreddit_data_http_429_error():
    with patch('httpx.get') as mock_get:
        mock_get.return_value.status_code = 429
        mock_get.return_value.raise_for_status.side_effect = httpx.HTTPError(response=mock_get.return_value)

        with pytest.raises(httpx.HTTPError):
            get_subreddit_data("python", limit=1, age="new", wanted_data=["title"])