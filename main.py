import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread

# Bot configuration
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = '!'
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
    'cogs.help'
]

class IndieGOBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=intents)
        
    async def setup_hook(self):
        # Register slash commands
        await self.tree.sync()
        
        # Load cogs
        for extension in initial_extensions:
            try:
                await self.load_extension(extension)
                print(f'Loaded {extension}')
            except Exception as e:
                print(f'Failed to load {extension}: {e}')

bot = IndieGOBot()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="for /help"
    ))

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
