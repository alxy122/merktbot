import pytest
from unittest.mock import Mock, patch

from music.audio_manager import AudioManager


@pytest.fixture
def audio_manager():
    return AudioManager()


@patch('music.audio_manager.youtube_dl.YoutubeDL')
@patch('music.audio_manager.FFmpegPCMAudio')
def test_play_youtube_url(mock_ffmpeg, mock_ydl, audio_manager):
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    mock_voice_client = Mock()
    audio_manager.voice_client = mock_voice_client

    mock_ydl_instance = mock_ydl.return_value.__enter__.return_value
    mock_ydl_instance.extract_info.return_value = {'url': 'mock_audio_url'}

    audio_manager.play_youtube_url(url)

    mock_ydl.assert_called_once_with({'format': 'bestaudio/best', 'quiet': True})
    mock_ydl_instance.extract_info.assert_called_once_with(url, download=False)
    mock_ffmpeg.assert_called_once_with('mock_audio_url', options='-vn')
    mock_voice_client.play.assert_called_once()

def test_fail_play_youtube_url(audio_manager):
    url = "https://www.youtube.com/watch?v=invalid_url"
    mock_voice_client = Mock()
    audio_manager.voice_client = mock_voice_client

    with patch('music.audio_manager.youtube_dl.YoutubeDL') as mock_ydl, \
         patch('music.audio_manager.FFmpegPCMAudio') as mock_ffmpeg:
        mock_ydl_instance = mock_ydl.return_value.__enter__.return_value
        mock_ydl_instance.extract_info.side_effect = Exception("Failed to extract info")

        with pytest.raises(Exception, match="Failed to extract info"):
            audio_manager.play_youtube_url(url)

        mock_ydl_instance.extract_info.assert_called_once_with(url, download=False)
        mock_ffmpeg.assert_not_called()
        mock_voice_client.play.assert_not_called()

def test_play_next_on_fail(audio_manager):
    audio_manager.queue = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://www.youtube.com/watch?v=another_song"
    ]
    mock_voice_client = Mock()
    audio_manager.voice_client = mock_voice_client

    with patch('music.audio_manager.youtube_dl.YoutubeDL') as mock_ydl, \
         patch('music.audio_manager.FFmpegPCMAudio') as mock_ffmpeg:
        mock_ydl_instance = mock_ydl.return_value.__enter__.return_value
        mock_ydl_instance.extract_info.return_value = {'url': 'mock_audio_url'}
        mock_voice_client.play.side_effect = lambda *args, **kwargs: kwargs['after'](Exception("Playback error"))

        audio_manager.play_youtube_url(audio_manager.queue[0])

        mock_ydl.assert_called_once_with({'format': 'bestaudio/best', 'quiet': True})
        mock_ydl_instance.extract_info.assert_called_once_with(audio_manager.queue[0], download=False)
        mock_ffmpeg.assert_called_once_with('mock_audio_url', options='-vn')
        mock_voice_client.play.assert_called_once()
        assert audio_manager.queue == ["https://www.youtube.com/watch?v=another_song"]
        audio_manager.voice_client.play.assert_called_once()
