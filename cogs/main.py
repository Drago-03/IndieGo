from flask import Flask
from threading import Thread
from dotenv import load_dotenv
from discord.ext import commands
import discord
import os

from config import INSTALL_URL

# Load environment variables from .env file
load_dotenv()

# Bot configuration
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = '.'
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# List of initial extensions to load
initial_extensions = [
    'cogs.general',
    'cogs.moderation',
    'cogs.fun',
    'cogs.admin',
    'cogs.tickets',
    'cogs.logging',
    'cogs.ai_assistant',
    'cogs.coding_help',
    'cogs.help',
    'cogs.base',
    'cogs.errors'
]

BOT_WEBSITE = "https://drago-03.github.io/IndieGo-Website/"

class IndieGOBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=intents, help_command=None)  # Disable default help command
        
    async def setup_hook(self):
        # Register slash commands
        for extension in initial_extensions:
            try:
                await self.load_extension(extension)
                print(f'Loaded {extension}')
            except Exception as e:
                print(f'Failed to load {extension}: {e}')
        await self.tree.sync()

bot = IndieGOBot()

# Flask web server to keep the bot running
app = Flask('')

@app.route('/')
def home():
    return "IndieGO Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)