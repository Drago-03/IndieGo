import discord
from discord.ext import commands
from config import TOKEN, PREFIX
from discord import app_commands

# Set up intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

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

# Example slash command
@bot.tree.command(name="help", description="Show bot help and commands")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="IndieGO Bot Help",
        description="Here are my available commands:",
        color=discord.Color.blue()
    )
    # Add command categories...
    await interaction.response.send_message(embed=embed)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name="for .help | /help"
    ))

bot.run(TOKEN)