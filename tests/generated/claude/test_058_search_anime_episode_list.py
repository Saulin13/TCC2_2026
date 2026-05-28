import pytest
from unittest.mock import Mock, patch
from web_programming.fetch_anime_and_play import search_anime_episode_list


@pytest.fixture
def mock_html_with_episodes():
    return """
    <html>
        <body>
            <ul id="episode_related">
                <li>
                    <a href="/episode/kimetsu-no-yaiba-1">Link</a>
                    <div class="name">Episode 1</div>
                </li>
                <li>
                    <a href="/episode/kimetsu-no-yaiba-2">Link</a>
                    <div class="name">Episode 2</div>
                </li>
                <li>
                    <a href="/episode/kimetsu-no-yaiba-3">Link</a>
                    <div class="name">Episode 3</div>
                </li>
            </ul>
        </body>
    </html>
    """


@pytest.fixture
def mock_html_no_episode_ul():
    return """
    <html>
        <body>
            <div>No episodes here</div>
        </body>
    </html>
    """


@pytest.fixture
def mock_html_empty_episode_ul():
    return """
    <html>
        <body>
            <ul id="episode_related">
            </ul>
        </body>
    </html>
    """


@pytest.fixture
def mock_html_with_spaces_in_title():
    return """
    <html>
        <body>
            <ul id="episode_related">
                <li>
                    <a href="/episode/test-1">Link</a>
                    <div class="name">Episode   1   Title</div>
                </li>
            </ul>
        </body>
    </html>
    """


@pytest.fixture
def mock_html_with_incomplete_episodes():
    return """
    <html>
        <body>
            <ul id="episode_related">
                <li>
                    <a href="/episode/test-1">Link</a>
                    <div class="name">Episode 1</div>
                </li>
                <li>
                    <div class="name">Episode 2 No Link</div>
                </li>
                <li>
                    <a href="/episode/test-3">Link</a>
                </li>
                <li>
                    <a href="/episode/test-4">Link</a>
                    <div class="name">Episode 4</div>
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
    assert result[0] == {"title": "Episode1", "url": "/episode/kimetsu-no-yaiba-1"}
    assert result[1] == {"title": "Episode2", "url": "/episode/kimetsu-no-yaiba-2"}
    assert result[2] == {"title": "Episode3", "url": "/episode/kimetsu-no-yaiba-3"}


@patch('web_programming.fetch_anime_and_play.httpx.get')
def test_search_anime_episode_list_removes_spaces(mock_get, mock_html_with_spaces_in_title):
    mock_response = Mock()
    mock_response.text = mock_html_with_spaces_in_title
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = search_anime_episode_list("/anime/test-anime")

    assert len(result) == 1
    assert result[0]["title"] == "Episode1Title"
    assert result[0]["url"] == "/episode/test-1"


@patch('web_programming.fetch_anime_and_play.httpx.get')
def test_search_anime_episode_list_empty_ul(mock_get, mock_html_empty_episode_ul):
    mock_response = Mock()
    mock_response.text = mock_html_empty_episode_ul
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = search_anime_episode_list("/anime/empty-anime")

    assert isinstance(result, list)
    assert len(result) == 0


@patch('web_programming.fetch_anime_and_play.httpx.get')
def test_search_anime_episode_list_no_episode_ul_raises_error(mock_get, mock_html_no_episode_ul):
    mock_response = Mock()
    mock_response.text = mock_html_no_episode_ul
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    with pytest.raises(ValueError, match="Could not find any anime eposiodes"):
        search_anime_episode_list("/anime/nonexistent-anime")


@patch('web_programming.fetch_anime_and_play.httpx.get')
def test_search_anime_episode_list_incomplete_episodes(mock_get, mock_html_with_incomplete_episodes):
    mock_response = Mock()
    mock_response.text = mock_html_with_incomplete_episodes
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = search_anime_episode_list("/anime/test-anime")

    assert len(result) == 2
    assert result[0] == {"title": "Episode1", "url": "/episode/test-1"}
    assert result[1] == {"title": "Episode4", "url": "/episode/test-4"}


@patch('web_programming.fetch_anime_and_play.httpx.get')
def test_search_anime_episode_list_http_error(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = Exception("HTTP 404 Not Found")
    mock_get.return_value = mock_response

    with pytest.raises(Exception, match="HTTP 404 Not Found"):
        search_anime_episode_list("/anime/invalid-endpoint")


@patch('web_programming.fetch_anime_and_play.httpx.get')
def test_search_anime_episode_list_with_different_endpoint(mock_get, mock_html_with_episodes):
    mock_response = Mock()
    mock_response.text = mock_html_with_episodes
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = search_anime_episode_list("/anime/naruto")

    assert isinstance(result, list)
    assert len(result) == 3