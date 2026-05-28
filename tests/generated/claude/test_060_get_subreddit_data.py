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
                        "author": "user1",
                        "score": 100,
                        "url": "https://reddit.com/test1",
                        "num_comments": 50,
                        "created_utc": 1234567890
                    }
                },
                {
                    "data": {
                        "title": "Test Post 2",
                        "author": "user2",
                        "score": 200,
                        "url": "https://reddit.com/test2",
                        "num_comments": 75,
                        "created_utc": 1234567900
                    }
                }
            ]
        }
    }


@pytest.fixture
def mock_valid_terms():
    """Mock valid_terms that should be available in the module"""
    return {"title", "author", "score", "url", "num_comments", "created_utc"}


@patch("web_programming.reddit.httpx.get")
@patch("web_programming.reddit.valid_terms", {"title", "author", "score", "url", "num_comments", "created_utc"})
def test_get_subreddit_data_default_params(mock_get, mock_reddit_response):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_reddit_response
    mock_get.return_value = mock_response
    
    result = get_subreddit_data("python")
    
    assert len(result) == 1
    assert 0 in result
    assert result[0]["data"]["title"] == "Test Post 1"
    mock_get.assert_called_once()


@patch("web_programming.reddit.httpx.get")
@patch("web_programming.reddit.valid_terms", {"title", "author", "score", "url", "num_comments", "created_utc"})
def test_get_subreddit_data_with_limit(mock_get, mock_reddit_response):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_reddit_response
    mock_get.return_value = mock_response
    
    result = get_subreddit_data("python", limit=2)
    
    assert len(result) == 2
    assert 0 in result
    assert 1 in result
    assert result[0]["data"]["title"] == "Test Post 1"
    assert result[1]["data"]["title"] == "Test Post 2"


@patch("web_programming.reddit.httpx.get")
@patch("web_programming.reddit.valid_terms", {"title", "author", "score", "url", "num_comments", "created_utc"})
def test_get_subreddit_data_with_age_parameter(mock_get, mock_reddit_response):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_reddit_response
    mock_get.return_value = mock_response
    
    result = get_subreddit_data("python", limit=1, age="hot")
    
    assert len(result) == 1
    call_args = mock_get.call_args
    assert "hot.json" in call_args[0][0]


@patch("web_programming.reddit.httpx.get")
@patch("web_programming.reddit.valid_terms", {"title", "author", "score", "url", "num_comments", "created_utc"})
def test_get_subreddit_data_with_wanted_data(mock_get, mock_reddit_response):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_reddit_response
    mock_get.return_value = mock_response
    
    result = get_subreddit_data("python", limit=2, wanted_data=["title", "author"])
    
    assert len(result) == 2
    assert result[0] == {"title": "Test Post 1", "author": "user1"}
    assert result[1] == {"title": "Test Post 2", "author": "user2"}
    assert "score" not in result[0]
    assert "url" not in result[1]


@patch("web_programming.reddit.httpx.get")
@patch("web_programming.reddit.valid_terms", {"title", "author", "score", "url", "num_comments", "created_utc"})
def test_get_subreddit_data_with_single_wanted_data(mock_get, mock_reddit_response):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_reddit_response
    mock_get.return_value = mock_response
    
    result = get_subreddit_data("python", limit=1, wanted_data=["title"])
    
    assert result[0] == {"title": "Test Post 1"}


@patch("web_programming.reddit.valid_terms", {"title", "author", "score"})
def test_get_subreddit_data_invalid_search_term():
    with pytest.raises(ValueError) as exc_info:
        get_subreddit_data("python", wanted_data=["title", "invalid_field"])
    
    assert "Invalid search term" in str(exc_info.value)
    assert "invalid_field" in str(exc_info.value)


@patch("web_programming.reddit.valid_terms", {"title", "author"})
def test_get_subreddit_data_multiple_invalid_search_terms():
    with pytest.raises(ValueError) as exc_info:
        get_subreddit_data("python", wanted_data=["invalid1", "title", "invalid2"])
    
    error_message = str(exc_info.value)
    assert "Invalid search term" in error_message
    assert "invalid1" in error_message
    assert "invalid2" in error_message


@patch("web_programming.reddit.httpx.get")
@patch("web_programming.reddit.valid_terms", {"title", "author"})
def test_get_subreddit_data_http_error(mock_get):
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Not Found", request=Mock(), response=mock_response
    )
    mock_get.return_value = mock_response
    
    with pytest.raises(httpx.HTTPStatusError):
        get_subreddit_data("nonexistent_subreddit")


@patch("web_programming.reddit.httpx.get")
@patch("web_programming.reddit.valid_terms", {"title", "author"})
def test_get_subreddit_data_rate_limit(mock_get, mock_reddit_response):
    mock_response = Mock()
    mock_response.status_code = 429
    mock_response.json.return_value = mock_reddit_response
    mock_get.return_value = mock_response
    
    with pytest.raises(httpx.HTTPError):
        get_subreddit_data("python")


@patch("web_programming.reddit.httpx.get")
@patch("web_programming.reddit.valid_terms", {"title", "author", "score"})
def test_get_subreddit_data_empty_wanted_data_list(mock_get, mock_reddit_response):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_reddit_response
    mock_get.return_value = mock_response
    
    result = get_subreddit_data("python", limit=1, wanted_data=[])
    
    assert len(result) == 1
    assert result[0]["data"]["title"] == "Test Post 1"


@patch("web_programming.reddit.httpx.get")
@patch("web_programming.reddit.valid_terms", {"title", "author", "score"})
def test_get_subreddit_data_top_age(mock_get, mock_reddit_response):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_reddit_response
    mock_get.return_value = mock_response
    
    result = get_subreddit_data("python", limit=1, age="top")
    
    call_args = mock_get.call_args
    assert "top.json" in call_args[0][0]
    assert "limit=1" in call_args[0][0]