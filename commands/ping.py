from typing import Callable, Coroutine, Any
from discord import Interaction, Object
from discord.ext.commands import Bot

class PingCommand:
    def __init__(self, client: Bot, guild_id: int, *args, **kwargs) -> None:  # noqa
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
            await interaction.response.send_message(f"Pong! {ping:.2f}ms <:emoji_name:1328063105799950336>")  # noqa

        return command
