import discord
from discord.ext import commands
from config import TOKEN, PREFIX
from discord import app_commands

# Set up intents
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

bot.run(TOKEN)