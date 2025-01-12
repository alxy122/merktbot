import importlib
import inspect
import os
import pathlib
from discord import Intents, Object
from discord.ext.commands import Bot
from dotenv import load_dotenv
import discord

from music.AudioManager import AudioManager

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Verwende Bot anstelle von Client, um auf tree zugreifen zu können
intents = Intents.default()
Intents.message_content = True
client = Bot(command_prefix="!", intents=intents)
client.activity = discord.Activity(type=discord.ActivityType.watching, name="the 0 grow on the tree")
guild_id = 701707921922326568

audio_manager = AudioManager()


def get_commands():
    # Dynamically load all command modules from the 'commands' directory
    commands_folder = pathlib.Path(__file__).parent / "commands"
    c = []

    # Ensure the commands directory exists
    if not commands_folder.exists():
        return c

    for command_file in commands_folder.glob("*.py"):
        module_name = f"commands.{command_file.stem}"
        try:
            # Dynamically import the module
            module = importlib.import_module(module_name)

            # Look for classes that inherit from BaseCommand or are instances of MusicCommand
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj):
                    if hasattr(obj, 'register_command'):
                        command_instance = obj(client, guild_id, audio_manager)
                        c.append(command_instance)
        except Exception as e:
            print(f"Failed to load module {module_name}: {e}")

    return c


@client.event
async def on_ready():
    for guild in client.guilds:
        print(f"Connected to guild: {guild.name}, Guild ID: {guild.id}")

    for command in get_commands():
        command.register_command()



    await client.tree.sync(guild=Object(id=guild_id))
    # Also sync the tree for all other guilds the bot is connected to but this is slower
    await client.tree.sync()

    print("Ready!")

client.run(TOKEN)
