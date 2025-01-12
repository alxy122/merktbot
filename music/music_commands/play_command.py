from typing import Callable, Coroutine, Any
import discord
from discord import Interaction, Object, app_commands
from discord.ext.commands import Bot


class PlayCommand:
    """
    A class to represent the PlayCommand.

    Attributes
    ----------
    bot : Bot
        The discord client object.
    name : str
        The name of the command.
    description : str
        The description of the command.
    guild_id : int
        The guild ID to register the command.
    audio_manager
        The audio manager object.

    Methods
    -------
    register_command()
        Register the play command.
    """
    def __init__(self, bot: Bot, guild_id: int, audio_manager, *args, **kwargs) -> None:  # noqa
        """
        Initialize the PlayCommand with the client, guild_id, audio_manager, and other arguments.

        :param bot: The discord client object.
        :type bot: Bot
        :param guild_id: The guild ID to register the command in.
        :type guild_id: int
        :param audio_manager: The audio manager object.
        :type audio_manager: AudioManager
        """
        self.bot = bot
        self.name = "play"
        self.description = "Plays a URL"
        self.guild_id = guild_id
        self.audio_manager = audio_manager

    def register_command(self) -> Callable[[Interaction, str], Coroutine[Any, Any, None]]:
        """
        Register the play command.
        :return: The command function.
        :rtype: Callable[[Interaction, str], Coroutine[Any, Any, None]]
        """
        @self.bot.tree.command(
            name=self.name,
            description=self.description,
            guild=Object(id=self.guild_id)
        )
        @app_commands.describe(url="The URL of the music to play.")
        async def command(interaction: Interaction, url: str):
            """
            The command function.
            :param interaction: The interaction object.
            :type interaction: Interaction
            :param url: The URL of the music to play.
            :type url: str
            """
            try:
                voice_channel = interaction.user.voice.channel
                if not voice_channel:
                    await interaction.response.send_message("You are not connected to a voice channel.")  # noqa
                    return

                voice_client = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
                if not voice_client:
                    voice_client = await voice_channel.connect()

                self.audio_manager.set_voice_client(voice_client)
                self.audio_manager.add_to_queue(url)
                await interaction.response.send_message(f"Added {url} to the queue.")  # noqa
            except discord.errors.NotFound:
                await interaction.followup.send(f"Sorry, the interaction has timed out. Could not add {url} to the queue.")
            except Exception as e:
                await interaction.followup.send(f"An error occurred: {e}")

        return command
