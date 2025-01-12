from typing import Callable, Coroutine, Any
from discord import Interaction, Object, app_commands
from discord.ext.commands import Bot

class QueueCommand:
    def __init__(self, bot: Bot, guild_id: int, audio_manager, *args, **kwargs) -> None:  # noqa
        self.bot = bot
        self.name = "queue"
        self.description = "Shows the current queue."
        self.guild_id = guild_id
        self.audio_manager = audio_manager

    def register_command(self) -> Callable[[Interaction], Coroutine[Any, Any, None]]:
        @self.bot.tree.command(
            name=self.name,
            description=self.description,
            guild=Object(id=self.guild_id)
        )
        async def command(interaction: Interaction):
            queue = self.audio_manager.get_queue()
            if not queue:
                await interaction.response.send_message("The queue is empty.")  # noqa
            else:
                message = "Current queue:\n"
                for i, song in enumerate(queue):
                    message += f"{i+1}. {song}\n"
                await interaction.response.send_message(message)  # noqa
        return command