from typing import List
from discord import FFmpegPCMAudio, VoiceClient
import yt_dlp as youtube_dl

class AudioManager:
    def __init__(self):
        self.queue: List[str] = []
        self.voice_client: VoiceClient = None  # noqa

    def add_to_queue(self, url: str) -> None:
        self.queue.append(url)
        if not self.voice_client.is_playing():
            self.play_next()

    def set_voice_client(self, voice_client: VoiceClient) -> None:
        self.voice_client = voice_client

    def play_next(self):
        if not self.queue:
            return
        url = self.queue.pop(0)
        self.play_youtube_url(url)

    def stop(self):
        self.queue = []
        if self.voice_client and self.voice_client.is_connected():
            self.voice_client.disconnect()

    def skip(self):
        """Skip the current song and play the next one in the queue."""
        if not self.voice_client:
            return
        if self.voice_client.is_playing():
            self.voice_client.stop()  # Stop the current song
        self.play_next()  # Start the next song in the queue

    def get_queue(self) -> List[str]:
        return self.queue

    def play_youtube_url(self, url: str) -> None:
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
                import gc
                gc.collect()

            self.voice_client.play(FFmpegPCMAudio(audio_url, **ffmpeg_options), after=after_playback)

