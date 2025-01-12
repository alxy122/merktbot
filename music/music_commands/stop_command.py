from typing import Callable, Coroutine, Any
from discord import Interaction, Object
from discord.ext.commands import Bot
from music.AudioManager import AudioManager


class SkipCommand:
    """
    SkipCommand class is used to skip the current song.

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
    def __init__(self, bot: Bot, guild_id: int, audio_manager:AudioManager, *args, **kwargs) -> None:
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
        self.name = "stop"
        self.description = "Stops the player."
        self.guild_id = guild_id
        self.audio_manager = audio_manager

        assert len(args) == 0 and len(kwargs) == 0, "No additional arguments are allowed."

    def __str__(self):
        return f"SkipCommand(name={self.name}, description={self.description}, guild_id={self.guild_id})"

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
            Stop the player.
            :param interaction: The interaction object.
            :type interaction: Interaction
            """
            self.audio_manager.stop()
            await interaction.response.send_message(f"Stopped the player.")  # noqa
        return command
