import pytest

from music.audio_manager import AudioManager


@pytest.fixture
def audio_manager():
    return AudioManager()

def test_get_empty_queue(audio_manager):
    assert audio_manager.get_queue() == []

def test_get_queue_with_songs(audio_manager):
    audio_manager.queue = ["https://www.youtube.com/watch?v=dQw4w9WgXcQ", "https://www.youtube.com/watch?v=6_b7RDuLwcI"]

    assert audio_manager.get_queue() == ["https://www.youtube.com/watch?v=dQw4w9WgXcQ", "https://www.youtube.com/watch?v=6_b7RDuLwcI"]