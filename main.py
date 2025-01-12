import os
from discord import Client, Intents
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

print(TOKEN)


class MyClient(Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

intents = Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)