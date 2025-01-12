from typing import Callable, Coroutine, Any
from discord import Interaction, Object
from discord.ext.commands import Bot
from music.AudioManager import AudioManager

class SkipCommand:
    def __init__(self, bot: Bot, guild_id: int, audio_manager:AudioManager, *args, **kwargs) -> None:  # noqa
        self.bot = bot
        self.name = "stop"
        self.description = "Stops the player."
        self.guild_id = guild_id
        self.audio_manager = audio_manager

    def register_command(self) -> Callable[[Interaction], Coroutine[Any, Any, None]]:
        @self.bot.tree.command(
            name=self.name,
            description=self.description,
            guild=Object(id=self.guild_id)
        )
        async def command(interaction: Interaction):
            if self.audio_manager.
            self.audio_manager.stop()
            await interaction.response.send_message(f"Stopped the player.")  # noqa
        return command
