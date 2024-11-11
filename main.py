import discord
from discord.ext import commands
from config import TOKEN, PREFIX

# Set up intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Load cogs
initial_extensions = [
    'cogs.moderation',
    'cogs.tickets',
    'cogs.coding_help',
    'cogs.fun',
]

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            print(f'Loaded {extension}')
        except Exception as e:
            print(f'Failed to load {extension}: {e}')

bot.run(TOKEN)