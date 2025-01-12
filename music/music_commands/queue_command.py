"""
This module contains the QueueCommand class, which represents a command
that shows the current queue in a Discord bot.
"""

from typing import Callable, Coroutine, Any
from discord import Interaction, Object
from discord.ext.commands import Bot


class QueueCommand:
    """
    Command to show the current queue.

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
        Register the queue command.
    """
    def __init__(self, bot: Bot,
                 guild_id: int,
                 audio_manager,
                 *args, **kwargs) -> None:
        """
        Initialize the QueueCommand with the client, guild_id, audio_manager, and other arguments.
        :param bot: The discord client object.
        :type bot: Bot
        :param guild_id: The guild ID to register the command in.
        :type guild_id: int
        :param audio_manager: The audio manager object.
        :type audio_manager: AudioManager
        """
        self.bot = bot
        self.name = "queue"
        self.description = "Shows the current queue."
        self.guild_id = guild_id
        self.audio_manager = audio_manager

        assert len(args) == 0 and len(kwargs) == 0, "No additional arguments are allowed."

    def __str__(self):
        return (f"QueueCommand(name={self.name}, "
                f"description={self.description}, "
                f"guild_id={self.guild_id})")

    def register_command(self) -> Callable[[Interaction], Coroutine[Any, Any, None]]:
        """
        Register the queue command.
        :return: The command function.
        :rtype: Callable[[Interaction], Coroutine[Any, Any, None]]
        """
        @self.bot.tree.command(
            name=self.name,
            description=self.description,
            guild=Object(id=self.guild_id)
        )
        async def command(interaction: Interaction) -> None:
            """
            The command function.
            :param interaction: The interaction object.
            :type interaction: Interaction
            """
            queue = self.audio_manager.get_queue()
            if not queue:
                await interaction.response.send_message("The queue is empty.")  # noqa
            else:
                message = "Current queue:\n"
                for i, song in enumerate(queue):
                    message += f"{i+1}. {song}\n"
                await interaction.response.send_message(message)  # noqa
        return command
