import pytest
from unittest.mock import Mock

from music.audio_manager import AudioManager


@pytest.fixture
def audio_manager():
    return AudioManager()

def test_set_voice_client(audio_manager):
    voice_client = Mock()
    audio_manager.set_voice_client(voice_client)
    assert audio_manager.voice_client == voice_client