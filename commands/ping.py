from typing import Callable, Coroutine, Any
from discord import Interaction, Object
from discord.ext.commands import Bot

class PingCommand:
    """
    A class to represent the PingCommand.

    Attributes
    ----------
    client : Bot
        The discord client object.
    name : str
        The name of the command.
    description : str
        The description of the command.
    guild_id : int
        The guild ID to register the command

    Methods
    -------
    register_command()
        Register the specific command function within the bot's command tree.
    """
    def __init__(self, client: Bot, guild_id: int, *args, **kwargs) -> None:
        """
        Initialize the HelloCommand with the client and guild_id.

        :param client: The discord client object.
        :type client: Bot
        :param guild_id: The guild ID to register the command in.
        :type guild_id: int
        """
        self.client = client
        self.name = "ping"
        self.description = "Pong!"
        self.guild_id = guild_id

        assert len(args) == 0 and len(kwargs) == 0, "No additional arguments are allowed."

    def __str__(self):
        return f"PingCommand(name={self.name}, description={self.description}, guild_id={self.guild_id})"

    def register_command(self) -> Callable[[Interaction], Coroutine[Any, Any, None]]:
        """
        Register the specific command function within the bot's command tree.

        :return: The command function to be registered.
        :rtype: Callable[[Interaction], Coroutine[Any, Any, None]]
        """

        @self.client.tree.command(
            name=self.name,
            description=self.description,
            guild=Object(id=self.guild_id)
        )
        async def command(interaction: Interaction):
            """
            Call the method (which is specific to the command)

            :param interaction:
            :return:
            """
            ping = self.client.latency * 1000
            await interaction.response.send_message(  # noqa
                f"Pong! {ping:.2f}ms <:emoji_name:1328063105799950336>")

        return command
