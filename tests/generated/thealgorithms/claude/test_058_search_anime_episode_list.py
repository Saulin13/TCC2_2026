import pytest
import httpx
from unittest.mock import Mock, patch
from web_programming.fetch_anime_and_play import search_anime_episode_list


@pytest.fixture
def mock_html_with_episodes():
    return """
    <html>
        <body>
            <ul id="episode_related">
                <li>
                    <a href="/episode/kimetsu-no-yaiba-1">Episode 1</a>
                    <div class="name">Episode 1: Cruelty</div>
                </li>
                <li>
                    <a href="/episode/kimetsu-no-yaiba-2">Episode 2</a>
                    <div class="name">Episode 2: Trainer</div>
                </li>
                <li>
                    <a href="/episode/kimetsu-no-yaiba-3">Episode 3</a>
                    <div class="name">Episode 3: Sabito and Makomo</div>
                </li>
            </ul>
        </body>
    </html>
    """


@pytest.fixture
def mock_html_empty_episodes():
    return """
    <html>
        <body>
            <ul id="episode_related">
            </ul>
        </body>
    </html>
    """


@pytest.fixture
def mock_html_no_episode_list():
    return """
    <html>
        <body>
            <div>No episodes here</div>
        </body>
    </html>
    """


@pytest.fixture
def mock_html_malformed_episodes():
    return """
    <html>
        <body>
            <ul id="episode_related">
                <li>
                    <a href="/episode/test-1">Episode 1</a>
                    <div class="name">Valid Episode</div>
                </li>
                <li>
                    <div class="name">Missing Link</div>
                </li>
                <li>
                    <a href="/episode/test-2">Episode 2</a>
                </li>
                <li>
                    <a href="/episode/test-3">Episode 3</a>
                    <div class="name">Another Valid Episode</div>
                </li>
            </ul>
        </body>
    </html>
    """


@patch('web_programming.fetch_anime_and_play.httpx.get')
def test_search_anime_episode_list_normal_case(mock_get, mock_html_with_episodes):
    mock_response = Mock()
    mock_response.text = mock_html_with_episodes
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response
    
    result = search_anime_episode_list("/anime/kimetsu-no-yaiba")
    
    assert isinstance(result, list)
    assert len(result) == 3
    assert result[0] == {"title": "Episode1:Cruelty", "url": "/episode/kimetsu-no-yaiba-1"}
    assert result[1] == {"title": "Episode2:Trainer", "url": "/episode/kimetsu-no-yaiba-2"}
    assert result[2] == {"title": "Episode3:SabitoandMakomo", "url": "/episode/kimetsu-no-yaiba-3"}


@patch('web_programming.fetch_anime_and_play.httpx.get')
def test_search_anime_episode_list_empty_list(mock_get, mock_html_empty_episodes):
    mock_response = Mock()
    mock_response.text = mock_html_empty_episodes
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response
    
    result = search_anime_episode_list("/anime/empty-anime")
    
    assert isinstance(result, list)
    assert len(result) == 0


@patch('web_programming.fetch_anime_and_play.httpx.get')
def test_search_anime_episode_list_no_episode_ul_raises_error(mock_get, mock_html_no_episode_list):
    mock_response = Mock()
    mock_response.text = mock_html_no_episode_list
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response
    
    with pytest.raises(ValueError, match="Could not find any anime eposiodes"):
        search_anime_episode_list("/anime/nonexistent")


@patch('web_programming.fetch_anime_and_play.httpx.get')
def test_search_anime_episode_list_malformed_episodes(mock_get, mock_html_malformed_episodes):
    mock_response = Mock()
    mock_response.text = mock_html_malformed_episodes
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response
    
    result = search_anime_episode_list("/anime/test-anime")
    
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0] == {"title": "ValidEpisode", "url": "/episode/test-1"}
    assert result[1] == {"title": "AnotherValidEpisode", "url": "/episode/test-3"}


@patch('web_programming.fetch_anime_and_play.httpx.get')
def test_search_anime_episode_list_http_error(mock_get):
    mock_get.side_effect = httpx.HTTPStatusError(
        "404 Not Found",
        request=Mock(),
        response=Mock(status_code=404)
    )
    
    with pytest.raises(httpx.HTTPStatusError):
        search_anime_episode_list("/anime/invalid")


@patch('web_programming.fetch_anime_and_play.httpx.get')
def test_search_anime_episode_list_timeout(mock_get):
    mock_get.side_effect = httpx.TimeoutException("Request timed out")
    
    with pytest.raises(httpx.TimeoutException):
        search_anime_episode_list("/anime/slow-server")


@patch('web_programming.fetch_anime_and_play.httpx.get')
def test_search_anime_episode_list_with_spaces_in_title(mock_get):
    html_with_spaces = """
    <html>
        <body>
            <ul id="episode_related">
                <li>
                    <a href="/episode/test-1">Episode 1</a>
                    <div class="name">  Episode  1:  Title  With  Spaces  </div>
                </li>
            </ul>
        </body>
    </html>
    """
    mock_response = Mock()
    mock_response.text = html_with_spaces
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response
    
    result = search_anime_episode_list("/anime/test")
    
    assert len(result) == 1
    assert result[0]["title"] == "Episode1:TitleWithSpaces"
    assert " " not in result[0]["title"]