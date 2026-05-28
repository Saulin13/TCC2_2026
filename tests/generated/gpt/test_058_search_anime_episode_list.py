import pytest
from unittest.mock import patch, Mock
from web_programming.fetch_anime_and_play import search_anime_episode_list
from bs4 import BeautifulSoup

# Mock data for testing
mock_html = """
<ul id="episode_related">
    <li>
        <a href="/episode/1">Episode 1</a>
        <div class="name">Episode 1</div>
    </li>
    <li>
        <a href="/episode/2">Episode 2</a>
        <div class="name">Episode 2</div>
    </li>
</ul>
"""

mock_html_no_episodes = """
<ul id="episode_related">
</ul>
"""

mock_html_no_ul = """
<div id="not_episode_related">
    <li>
        <a href="/episode/1">Episode 1</a>
        <div class="name">Episode 1</div>
    </li>
</div>
"""

@pytest.fixture
def mock_httpx_get():
    with patch('httpx.get') as mock_get:
        yield mock_get

def test_search_anime_episode_list_normal_case(mock_httpx_get):
    mock_response = Mock()
    mock_response.text = mock_html
    mock_response.raise_for_status = Mock()
    mock_httpx_get.return_value = mock_response

    result = search_anime_episode_list("/anime/kimetsu-no-yaiba")
    expected = [
        {"title": "Episode1", "url": "/episode/1"},
        {"title": "Episode2", "url": "/episode/2"}
    ]
    assert result == expected

def test_search_anime_episode_list_no_episodes(mock_httpx_get):
    mock_response = Mock()
    mock_response.text = mock_html_no_episodes
    mock_response.raise_for_status = Mock()
    mock_httpx_get.return_value = mock_response

    result = search_anime_episode_list("/anime/empty-anime")
    assert result == []

def test_search_anime_episode_list_no_ul(mock_httpx_get):
    mock_response = Mock()
    mock_response.text = mock_html_no_ul
    mock_response.raise_for_status = Mock()
    mock_httpx_get.return_value = mock_response

    with pytest.raises(ValueError, match="Could not find any anime eposiodes with name"):
        search_anime_episode_list("/anime/no-ul")

def test_search_anime_episode_list_http_error(mock_httpx_get):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = Exception("HTTP Error")
    mock_httpx_get.return_value = mock_response

    with pytest.raises(Exception, match="HTTP Error"):
        search_anime_episode_list("/anime/http-error")