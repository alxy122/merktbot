from typing import Callable, Coroutine
from discord import Interaction, Object
from discord.ext.commands import Bot


class HelloCommand:
    """
    A class to represent the HelloCommand.

    Attributes
    ----------
    client : Bot
        The discord client object.
    name : str
        The name of the command.
    description : str
        The description of the command.
    guild_id : int
        The guild ID to register the
        command

    Methods
    -------
    register_command()
        Register the hello command.

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
        self.name = "hello"
        self.description = "Say hello!"
        self.guild_id = guild_id

        assert len(args) == 0 and len(kwargs) == 0, "No additional arguments are allowed."

    def __str__(self):
        return f"HelloCommand(name={self.name}, description={self.description}, guild_id={self.guild_id})"

    def register_command(self) -> Callable[[Interaction], Coroutine[None, None, None]]:
        """
        Register the hello command.

        :return: The command function.
        :rtype: Callable[[Interaction], Coroutine[None, None, None]]
        """

        @self.client.tree.command(
            name=self.name,
            description=self.description,
            guild=Object(id=self.guild_id)
        )
        async def command(interaction: Interaction):
            """
            The command function.
            :param interaction:
            :type interaction: Interaction
            """
            await interaction.response.send_message("Hello!")  # noqa

        return command
