import datetime
from typing import Callable, Coroutine, Any
from discord import Interaction, Object
from discord.ext.commands import Bot

class The1510Command:
    """
    A class to represent the 1510Command.

    Attributes
    ----------
    client : Bot
        The discord client object.
    name : str
        The name of the command.
    description : str
        The description of the command.
    guild_id : int
        The guild ID to register the command.

    Methods
    -------
    register_command()
        Register the specific command function within the bot's command tree.
    """
    def __init__(self, client:Bot, guild_id:int, *args, **kwargs) -> None:
        """
        Initialize the HelloCommand with the client and guild_id.

        :param client: The discord client object.
        :type client: Bot
        :param guild_id: The guild ID to register the command in.
        :type guild_id: int
        """

        self.client = client
        self.name="1510"
        self.description="When is the next 15:10?"
        self.guild_id=guild_id

        assert len(args) == 0 and len(kwargs) == 0, "No additional arguments are allowed."

    def __str__(self):
        return f"The1510Command(name={self.name}, description={self.description}, guild_id={self.guild_id})"

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
            now = datetime.datetime.now()
            next_1510 = now.replace(hour=15, minute=10, second=0, microsecond=0)

            if now >= next_1510:
                next_1510 += datetime.timedelta(days=1)

            time_difference = next_1510 - now
            hours, remainder = divmod(time_difference.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            if hours == 23 and minutes == 59:
                message = ("It's 15:10!\n"
                           "https://www.youtube.com/watch?v=FJdtXvW78os")
            else:
                message = (f"Time until next 15:10: {hours} hours, {minutes} minutes, and {seconds} seconds\n"
                           f"But be prepared\n"
                           f"https://www.youtube.com/watch?v=FJdtXvW78os")
            await interaction.response.send_message(message)  # noqa

        return command
