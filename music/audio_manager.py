"""
This module contains the AudioManager class, which manages the audio playback
in a Discord bot's voice channel.
"""

import gc
from typing import List
from discord import FFmpegPCMAudio, VoiceClient
import yt_dlp as youtube_dl


class AudioManager:
    """
    AudioManager is a class that manages the audio playback in a voice channel.
    It can add songs to a queue, play the next song in the queue, skip the current song,
    and stop the playback.

    Attributes:
    -----------
    queue : List[str]
        The list of URLs to play.
    voice_client : VoiceClient
        The voice client object.

    Methods:
    --------
    add_to_queue(url: str) -> None
        Add a song to the queue.
    set_voice_client(voice_client: VoiceClient) -> None
        Set the voice client object.
    play_next()
        Play the next song in the queue.
    stop()
        Stop the playback.
    skip()
        Skip the current song and play the next one in the queue.
    get_queue() -> List[str]
        Get the queue.
    play_youtube_url(url: str) -> None
        Play a song from a YouTube URL.
    """

    def __init__(self):
        """
        Initialize the AudioManager with an empty queue and a None voice client.
        """
        self.queue: List[str] = []
        self.voice_client: VoiceClient = None  # noqa

    def add_to_queue(self, url: str) -> None:
        """
        Add a song to the queue.
        :param url: The URL of the song.
        :type url: str
        :return:
        """
        self.queue.append(url)
        if not self.voice_client.is_playing():
            self.play_next()

    def set_voice_client(self, voice_client: VoiceClient) -> None:
        """
        Set the voice client object.
        :param voice_client: The voice client object.
        :type voice_client: VoiceClient
        """
        self.voice_client = voice_client

    def play_next(self) -> None:
        """
        Play the next song in the queue.
        """
        if not self.queue:
            return
        url = self.queue.pop(0)
        self.play_youtube_url(url)

    def stop(self) -> None:
        """
        Stop the playback.
        """
        self.queue = []
        if self.voice_client and self.voice_client.is_connected():
            self.voice_client.disconnect()

    def skip(self) -> None:
        """
        Skip the current song and play the next one in the queue.
        """
        if not self.voice_client:
            return
        if self.voice_client.is_playing():
            self.voice_client.stop()  # Stop the current song
        self.play_next()  # Start the next song in the queue

    def get_queue(self) -> List[str]:
        """
        Get the queue.
        :return: The queue.
        :rtype: List[str]
        """
        return self.queue

    def play_youtube_url(self, url: str) -> None:
        """
        Play a song from a YouTube URL.
        :param url:  The URL of the song.
        :type url: str
        """
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info['url']
            ffmpeg_options = {
                'options': '-vn'
            }

            def after_playback(error):
                if error:
                    print(f"Error during playback: {error}")
                # Call play_next to continue the queue
                self.play_next()
                # Force garbage collection (optional)
                gc.collect()

            self.voice_client.play(
                FFmpegPCMAudio(audio_url, **ffmpeg_options),
                after=after_playback)
