# Discord Music Bot 🎵

A Discord bot built with [discord.py](https://discordpy.readthedocs.io/) that can join voice channels, play music from YouTube, and manage a queue.

## Features
- Play music from YouTube URLs.
- Queue multiple songs.
- Skip, stop, and manage playback.
- Easy setup using a `.env` file for secure key management.

## Installation

Follow these steps to set up and run the bot on your system:

### Prerequisites
1. Python 3.8 or higher installed on your system.
2. [FFmpeg](https://ffmpeg.org/download.html) installed and added to your system's PATH.
3. A Discord bot application set up with a token. If you don’t have one, follow the [Discord Developer Portal guide](https://discordpy.readthedocs.io/en/stable/discord.html).

### Steps
1. **Clone the repository**:
   ```bash
   git clone -b master git@github.com:alxy122/merktbot.git
   cd merktbot
   ```

2. **Set up a virtual environment (optional but recommended)**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file**:
   In the project root, create a file named `.env` with the following contents:
   ```env
   DISCORD_TOKEN="your-discord-bot-token"
   DISCORD_GUILD="your-discord-guild-id"
   ```
   - Replace `your-discord-bot-token` with your bot's token.
   - Replace `your-discord-guild-id` with your server's guild ID.

5. **Run the bot**:
   ```bash
   python main.py
   ```

## Usage
1. Invite the bot to your server using the OAuth2 URL from the Discord Developer Portal.
2. Join a voice channel and use the bot's music commands (e.g., `/play <YouTube URL>`).

## Configuration
- **Environment Variables**:
  - `DISCORD_TOKEN`: The token for your Discord bot.
  - `DISCORD_GUILD`: The Guild ID (server ID) where the bot is active.
- **FFmpeg**:
  Ensure FFmpeg is installed and added to your system's PATH.

## Commands
| Command      | Description                           |
|--------------|---------------------------------------|
| `/play <url>`| Play a YouTube video or add to queue. |
| `/skip`      | Skip the current song.               |
| `/stop`      | Stop playback and clear the queue.   |
| `/queue`     | Show the current song queue.         |

## Troubleshooting
- **Bot not joining voice channels**: Ensure it has `Connect` and `Speak` permissions.
- **Audio issues**: Check if FFmpeg is installed and accessible from the command line.

## Contributing
Feel free to fork this repository and submit pull requests! For major changes, please open an issue first to discuss your ideas.

## License
This project is licensed under the [MIT License](LICENSE).

---

Enjoy listening to music with your Discord server! 🎶

