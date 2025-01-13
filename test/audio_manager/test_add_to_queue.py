import pytest
from unittest.mock import Mock

from music.audio_manager import AudioManager


@pytest.fixture
def audio_manager():
    return AudioManager()



def test_add_to_queue_single_song(audio_manager):
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    audio_manager.voice_client = Mock()
    audio_manager.voice_client.is_playing.return_value = False
    audio_manager.play_next = Mock()

    audio_manager.add_to_queue(url)

    assert url in audio_manager.queue
    audio_manager.play_next.assert_called_once()

def test_add_to_queue_while_playing(audio_manager):
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    audio_manager.voice_client = Mock()
    audio_manager.voice_client.is_playing.return_value = True
    audio_manager.play_next = Mock()

    audio_manager.add_to_queue(url)

    assert url in audio_manager.queue
    audio_manager.play_next.assert_not_called()

def test_add_to_queue_multiple_songs(audio_manager):
    url1 = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    url2 = "https://www.youtube.com/watch?v=6_b7RDuLwcI"
    audio_manager.voice_client = Mock()
    audio_manager.voice_client.is_playing.return_value = False
    audio_manager.play_next = Mock()

    audio_manager.add_to_queue(url1)
    audio_manager.voice_client.is_playing.return_value = True
    audio_manager.add_to_queue(url2)

    assert url1 in audio_manager.queue
    assert url2 in audio_manager.queue
    audio_manager.play_next.assert_called_once()

def test_add_to_queue_no_voice_client(audio_manager):
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    audio_manager.voice_client = None
    audio_manager.play_next = Mock()

    audio_manager.add_to_queue(url)

    assert url not in audio_manager.queue
    audio_manager.play_next.assert_not_called()

