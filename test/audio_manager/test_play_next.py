import pytest
from unittest.mock import Mock

from music.audio_manager import AudioManager


@pytest.fixture
def audio_manager():
    return AudioManager()

def test_play_next_with_empty_queue(audio_manager):
    audio_manager.voice_client = Mock()
    audio_manager.queue = []
    audio_manager.play_youtube_url = Mock()
    audio_manager.play_next()

    audio_manager.play_youtube_url.assert_not_called()

def test_play_next_with_song_in_queue(audio_manager):
    audio_manager.voice_client = Mock()
    audio_manager.queue = ["https://www.youtube.com/watch?v=dQw4w9WgXcQ"]
    audio_manager.play_youtube_url = Mock()
    audio_manager.play_next()

    audio_manager.play_youtube_url.assert_called_once()
    audio_manager.play_youtube_url.assert_called_with("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    assert audio_manager.queue == []

def test_play_next_with_multiple_songs_in_queue(audio_manager):
    audio_manager.voice_client = Mock()
    audio_manager.queue = ["https://www.youtube.com/watch?v=dQw4w9WgXcQ", "https://www.youtube.com/watch?v=6_b7RDuLwcI"]
    audio_manager.play_youtube_url = Mock()
    audio_manager.play_next()

    audio_manager.play_youtube_url.assert_called_once()
    audio_manager.play_youtube_url.assert_called_with("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    assert audio_manager.queue == ["https://www.youtube.com/watch?v=6_b7RDuLwcI"]