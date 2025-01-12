"""
This module is the main entry point for the Discord bot.
It loads all command modules from the 'commands' directory and
registers them with the bot.
The bot is then started and listens for incoming messages.

Attributes
----------
client : Bot
    The discord client object.
TOKEN : str
    The Discord bot token.
GUILD : str
    The Discord guild ID.
intents : Intents
    The Discord intents object.
audio_manager : AudioManager
    The audio manager object.

Methods
-------
get_commands(folder:str) -> List[CommandProtocol]
    This function dynamically loads all command modules from the specified folder.
on_ready()
    This function is called when the bot is ready.
"""

from typing import List, Protocol
import importlib
import inspect
import os
import pathlib
from discord import Intents, Object
from discord.ext.commands import Bot
from dotenv import load_dotenv
import discord
from music.audio_manager import AudioManager

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


class CommandProtocol(Protocol):
    """
    A protocol to represent a command.

    Methods
    -------
    register_command()
        Register the specific command function within the bot's command tree.
    """
    def register_command(self) -> None:
        """
        Register the specific command function within the bot's command tree.
        """

def get_commands(_client:Bot, _audio_manager:AudioManager, folder:str) -> List[CommandProtocol]:
    """
    This function dynamically loads all command modules from the specified folder.
    :param _audio_manager:
    :type _audio_manager: AudioManager
    :param _client: The discord client object.
    :type _client: Bot
    :param folder: The folder to load the command modules from.
    :type folder: str
    :return: A list of command instances.
    :rtype: List[object]
    """
    # Dynamically load all command modules from the 'commands' directory
    commands_folder = pathlib.Path(__file__).parent / folder
    c = []

    # Ensure the commands directory exists
    if not commands_folder.exists():
        return c

    for command_file in commands_folder.glob("*.py"):
        module_name = f"{folder.replace('/', '.')}.{command_file.stem}"
        try:
            # Dynamically import the module
            module = importlib.import_module(module_name)

            # Look for classes that inherit from BaseCommand or are instances of MusicCommand
            for _, obj in inspect.getmembers(module):
                if inspect.isclass(obj):
                    if hasattr(obj, 'register_command'):
                        command_instance = obj(_client, GUILD, _audio_manager)
                        c.append(command_instance)
        except ModuleNotFoundError:
            print(f"Failed to load module {module_name}: ModuleNotFoundError")
        except AttributeError:
            print(f"Failed to load module {module_name}: AttributeError")
        except (TypeError, ValueError) as e:
            print(f"Failed to load module {module_name}: {e}")
    return c

intents = Intents.default()
Intents.message_content = True
client = Bot(command_prefix="!", intents=intents)
client.activity = discord.Activity(
    type=discord.ActivityType.watching,
    name="the 0 grow on the tree")
audio_manager = AudioManager()


@client.event
async def on_ready() -> None:
    """
    This function is called when the bot is ready.
    """
    for guild in client.guilds:
        print(f"Connected to guild: {guild.name}, Guild ID: {guild.id}")

    for command in get_commands(_client=client,
                                _audio_manager=audio_manager,
                                folder="commands"):
        command.register_command()

    for command in get_commands(_client=client,
                                _audio_manager=audio_manager,
                                folder="music/music_commands"):
        command.register_command()

    await client.tree.sync(guild=Object(id=GUILD))
    # Also sync the tree for all other guilds the bot is connected to but this is slower
    await client.tree.sync()

    print("Ready!")

def main():
    """
    This function is the main entry point for the Discord bot.
    """
    client.run(TOKEN)

def dummy_for_pylint():
    """
    This function is to get rid of the
    0903: Too few public methods (1/2) (too-few-public-methods)
    error from pylint.
    """
    pass

if __name__ == "__main__":
    main()
