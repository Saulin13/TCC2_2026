import pytest
from web_programming.reddit import get_subreddit_data
import httpx
from unittest.mock import patch

# Mock response data
mock_response_data = {
    "data": {
        "children": [
            {
                "data": {
                    "title": "Test Post 1",
                    "author": "Author1",
                    "score": 100,
                }
            },
            {
                "data": {
                    "title": "Test Post 2",
                    "author": "Author2",
                    "score": 150,
                }
            },
        ]
    }
}

# Valid terms for testing
valid_terms = {"title", "author", "score"}

# Test normal case
def test_get_subreddit_data_normal():
    with patch('httpx.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response_data

        result = get_subreddit_data("testsubreddit", limit=2, age="new", wanted_data=["title", "author"])
        expected = {
            0: {"title": "Test Post 1", "author": "Author1"},
            1: {"title": "Test Post 2", "author": "Author2"},
        }
        assert result == expected

# Test edge case with no wanted_data
def test_get_subreddit_data_no_wanted_data():
    with patch('httpx.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response_data

        result = get_subreddit_data("testsubreddit", limit=1, age="new")
        expected = {0: mock_response_data["data"]["children"][0]}
        assert result == expected

# Test edge case with invalid search terms
def test_get_subreddit_data_invalid_search_terms():
    with pytest.raises(ValueError, match="Invalid search term: invalid_term"):
        get_subreddit_data("testsubreddit", limit=1, age="new", wanted_data=["invalid_term"])

# Test HTTP error handling
def test_get_subreddit_data_http_error():
    with patch('httpx.get') as mock_get:
        mock_get.return_value.status_code = 429
        mock_get.return_value.raise_for_status.side_effect = httpx.HTTPError("Too Many Requests")

        with pytest.raises(httpx.HTTPError, match="Too Many Requests"):
            get_subreddit_data("testsubreddit", limit=1, age="new")