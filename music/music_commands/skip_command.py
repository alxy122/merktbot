from typing import Callable, Coroutine, Any
from discord import Interaction, Object
from discord.ext.commands import Bot
from music.AudioManager import AudioManager


class SkipCommand:
    """
    A class used to represent a skip command.

    Attributes
    ----------
    bot : Bot
        the discord bot object
    name : str
        the name of the command
    description : str
        the description of the command
    guild_id : int
        the guild id
    audio_manager : AudioManager
        the audio manager object

    Methods
    -------
    register_command() -> Callable[[Interaction], Coroutine[Any, Any, None]]:
        Register the skip command.
    """
    def __init__(self, bot: Bot, guild_id: int, audio_manager:AudioManager, *args, **kwargs) -> None:  # noqa
        """
        Constructs all the necessary attributes for the skip command object.
        :param bot: The discord bot object.
        :type bot: Bot
        :param guild_id: The guild id.
        :type guild_id: int
        :param audio_manager: The audio manager object.
        :type audio_manager: AudioManager
        """
        self.bot = bot
        self.name = "skip"
        self.description = "Skip the current song."
        self.guild_id = guild_id
        self.audio_manager = audio_manager

    def register_command(self) -> Callable[[Interaction], Coroutine[Any, Any, None]]:
        """
        Register the skip command.
        :return: The skip command.
        :rtype: Callable[[Interaction], Coroutine[Any, Any, None]]
        """
        @self.bot.tree.command(
            name=self.name,
            description=self.description,
            guild=Object(id=self.guild_id)
        )
        async def command(interaction: Interaction) -> None:
            """
            Skip the current song.
            :param interaction: The interaction object.
            :type interaction: Interaction
            """
            self.audio_manager.skip()
            await interaction.response.send_message(f"Skipped the current song.")  # noqa
        return command
