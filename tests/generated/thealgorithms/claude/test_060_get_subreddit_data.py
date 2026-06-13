import pytest
import httpx
from unittest.mock import Mock, patch
from web_programming.reddit import get_subreddit_data


@pytest.fixture
def mock_reddit_response():
    """Create a mock Reddit API response"""
    return {
        "data": {
            "children": [
                {
                    "data": {
                        "title": "Test Post 1",
                        "author": "test_user1",
                        "score": 100,
                        "url": "https://reddit.com/test1",
                        "num_comments": 50
                    }
                },
                {
                    "data": {
                        "title": "Test Post 2",
                        "author": "test_user2",
                        "score": 200,
                        "url": "https://reddit.com/test2",
                        "num_comments": 75
                    }
                }
            ]
        }
    }


@pytest.fixture
def mock_httpx_get(mock_reddit_response):
    """Mock httpx.get to return a successful response"""
    with patch('web_programming.reddit.httpx.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_reddit_response
        mock_get.return_value = mock_response
        yield mock_get


def test_get_subreddit_data_default_parameters(mock_httpx_get, mock_reddit_response):
    result = get_subreddit_data("python")
    
    assert isinstance(result, dict)
    assert len(result) == 1
    assert 0 in result
    assert result[0] == mock_reddit_response["data"]["children"][0]
    mock_httpx_get.assert_called_once_with(
        "https://www.reddit.com/r/python/new.json?limit=1",
        headers={"User-agent": "A random string"},
        timeout=10
    )


def test_get_subreddit_data_with_limit(mock_httpx_get, mock_reddit_response):
    result = get_subreddit_data("python", limit=2)
    
    assert len(result) == 2
    assert 0 in result
    assert 1 in result
    assert result[0] == mock_reddit_response["data"]["children"][0]
    assert result[1] == mock_reddit_response["data"]["children"][1]


def test_get_subreddit_data_with_age_top(mock_httpx_get):
    get_subreddit_data("python", age="top")
    
    mock_httpx_get.assert_called_once_with(
        "https://www.reddit.com/r/python/top.json?limit=1",
        headers={"User-agent": "A random string"},
        timeout=10
    )


def test_get_subreddit_data_with_age_hot(mock_httpx_get):
    get_subreddit_data("python", age="hot")
    
    mock_httpx_get.assert_called_once_with(
        "https://www.reddit.com/r/python/hot.json?limit=1",
        headers={"User-agent": "A random string"},
        timeout=10
    )


def test_get_subreddit_data_with_wanted_data(mock_httpx_get, mock_reddit_response):
    result = get_subreddit_data("python", limit=2, wanted_data=["title", "author"])
    
    assert len(result) == 2
    assert result[0] == {"title": "Test Post 1", "author": "test_user1"}
    assert result[1] == {"title": "Test Post 2", "author": "test_user2"}


def test_get_subreddit_data_with_single_wanted_data(mock_httpx_get):
    result = get_subreddit_data("python", limit=1, wanted_data=["title"])
    
    assert result[0] == {"title": "Test Post 1"}


def test_get_subreddit_data_with_multiple_wanted_data(mock_httpx_get):
    result = get_subreddit_data("python", limit=1, wanted_data=["title", "score", "url"])
    
    assert result[0] == {
        "title": "Test Post 1",
        "score": 100,
        "url": "https://reddit.com/test1"
    }


def test_get_subreddit_data_invalid_search_term():
    with pytest.raises(ValueError) as exc_info:
        get_subreddit_data("python", wanted_data=["invalid_field"])
    
    assert "Invalid search term:" in str(exc_info.value)
    assert "invalid_field" in str(exc_info.value)


def test_get_subreddit_data_multiple_invalid_search_terms():
    with pytest.raises(ValueError) as exc_info:
        get_subreddit_data("python", wanted_data=["invalid1", "invalid2", "title"])
    
    error_message = str(exc_info.value)
    assert "Invalid search term:" in error_message
    assert "invalid1" in error_message
    assert "invalid2" in error_message


def test_get_subreddit_data_http_error():
    with patch('web_programming.reddit.httpx.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Not Found", request=Mock(), response=mock_response
        )
        mock_get.return_value = mock_response
        
        with pytest.raises(httpx.HTTPStatusError):
            get_subreddit_data("nonexistent_subreddit")


def test_get_subreddit_data_rate_limit_error():
    with patch('web_programming.reddit.httpx.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 429
        mock_get.return_value = mock_response
        
        with pytest.raises(httpx.HTTPError):
            get_subreddit_data("python")


def test_get_subreddit_data_empty_wanted_data_list(mock_httpx_get, mock_reddit_response):
    result = get_subreddit_data("python", limit=1, wanted_data=[])
    
    assert result[0] == mock_reddit_response["data"]["children"][0]


def test_get_subreddit_data_different_subreddit(mock_httpx_get):
    get_subreddit_data("learnpython", limit=1, age="new")
    
    mock_httpx_get.assert_called_once_with(
        "https://www.reddit.com/r/learnpython/new.json?limit=1",
        headers={"User-agent": "A random string"},
        timeout=10
    )