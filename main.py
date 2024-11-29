import discord
from discord.ext import commands
from config import TOKEN, PREFIX
from discord import app_commands
import aiosqlite
import asyncio
import logging
import sys
import traceback

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG for more detailed logs
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot.log')
    ]
)
logger = logging.getLogger('IndieGOBot')

# Set up intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class IndieGOBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=intents)
        self.initial_extensions = [
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
            'cogs.errors',
            'cogs.automod',
            'cogs.dm_interaction',
            'cogs.voice_channel',
            'cogs.ocr',
            'cogs.reddit'
        ]
        
    async def setup_hook(self):
        logger.info('Starting bot setup...')
        
        # Load cogs with detailed error handling
        for extension in self.initial_extensions:
            try:
                logger.debug(f'Attempting to load extension: {extension}')
                await self.load_extension(extension)
                logger.info(f'Successfully loaded extension: {extension}')
            except Exception as e:
                logger.error(f'Failed to load extension {extension}')
                logger.error(f'Error type: {type(e).__name__}')
                logger.error(f'Error message: {str(e)}')
                logger.error('Traceback:')
                logger.error(traceback.format_exc())
                # Continue loading other extensions instead of stopping
                continue

        # Try to sync commands after loading available cogs
        try:
            logger.info('Syncing command tree...')
            await self.tree.sync()
            logger.info('Command tree synced successfully')
        except Exception as e:
            logger.error(f'Failed to sync command tree: {str(e)}')
            logger.error(traceback.format_exc())

    async def on_ready(self):
        logger.info(f'{self.user} has connected to Discord!')
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="for .help | /help"
            )
        )

bot = IndieGOBot()

@bot.event
async def on_error(event, *args, **kwargs):
    logger.error(f'Error in event {event}:')
    logger.error(traceback.format_exc())

# Example slash command with error handling
@bot.tree.command(name="help", description="Show bot help and commands")
async def help(interaction: discord.Interaction):
    try:
        embed = discord.Embed(
            title="IndieGO Bot Help",
            description="Here are my available commands:",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        logger.error(f'Error in help command: {str(e)}')
        logger.error(traceback.format_exc())
        await interaction.response.send_message(
            "An error occurred while processing your request.",
            ephemeral=True
        )

async def main():
    try:
        logger.info('Starting bot...')
        async with bot:
            await bot.start(TOKEN)
    except Exception as e:
        logger.error(f'Fatal error in main: {str(e)}')
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Bot shutdown initiated by user')
    except Exception as e:
        logger.error(f'Unexpected error in runner: {str(e)}')
        logger.error(traceback.format_exc())