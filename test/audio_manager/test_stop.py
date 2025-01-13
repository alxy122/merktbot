import pytest
from unittest.mock import Mock

from music.audio_manager import AudioManager


@pytest.fixture
def audio_manager():
    return AudioManager()

def setup_voice_client(audio_manager, is_connected, is_playing):
    audio_manager.voice_client = Mock()
    audio_manager.voice_client.is_connected.return_value = is_connected
    audio_manager.voice_client.is_playing.return_value = is_playing
    audio_manager.voice_client.disconnect = Mock()

def test_stop_while_playing(audio_manager):
    audio_manager.queue = []
    audio_manager.voice_client = Mock()
    audio_manager.voice_client.return_value = True
    audio_manager.voice_client.is_connected.return_value = True
    audio_manager.voice_client.is_playing.return_value = True
    audio_manager.voice_client.disconnect = Mock()

    audio_manager.stop()

    assert audio_manager.queue == []
    audio_manager.voice_client.disconnect.assert_called_once()

def test_stop__with_song_in_queue(audio_manager):
    audio_manager.queue = ["https://www.youtube.com/watch?v=dQw4w9WgXcQ"]

    audio_manager.stop()

    assert audio_manager.queue == []

def test_stop_no_voice_client(audio_manager):
    audio_manager.queue = []
    audio_manager.voice_client = Mock()
    audio_manager.voice_client.is_connected.return_value = False
    audio_manager.voice_client.disconnect = Mock()

    audio_manager.stop()

    assert audio_manager.queue == []
    audio_manager.voice_client.disconnect.assert_not_called()
