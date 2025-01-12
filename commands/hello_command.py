from typing import Callable, Coroutine
from discord import Interaction, Object
from discord.ext.commands import Bot

class HelloCommand:
    def __init__(self, client: Bot, guild_id: int, *args, **kwargs) -> None:  # noqa
        """
        Initialize the HelloCommand with the client and guild_id.

        :param client: The discord client object.
        :type client: Bot
        :param guild_id: The guild ID to register the command in.
        :type guild_id: int
        """

        self.client = client
        self.name = "hello"
        self.description = "Say hello!"
        self.guild_id = guild_id

    def register_command(self) -> Callable[[Interaction], Coroutine[None, None, None]]:
        @self.client.tree.command(
            name=self.name,
            description=self.description,
            guild=Object(id=self.guild_id)
        )
        async def command(interaction: Interaction):
            await interaction.response.send_message("Hello!")  # noqa

        return command