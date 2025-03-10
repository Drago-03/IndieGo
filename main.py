import asyncio
import logging
import sys
import traceback

import discord
from discord.ext import commands

from config import TOKEN, PREFIX

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
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
intents.guilds = True

class IndieGOBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=PREFIX,
            intents=intents,
            help_command=None,  # Disable default help command
            application_id=1304755116255088670  # Add your bot's application ID here
        )
        self.initial_extensions = [
            'cogs.errors',      # Error handling first
            'cogs.base',        # Base functionality second
            'cogs.help',        # Help system third
            'cogs.general',     # Core features fourth
            'cogs.moderation',  # Moderation fifth
            'cogs.admin',       # Admin sixth
            'cogs.tickets',     # Tickets seventh
            'cogs.logging',     # Logging eighth
            'cogs.fun',         # Fun ninth
            'cogs.ai_assistant',# AI assistant tenth
            'cogs.coding_help', # Coding help eleventh
            'cogs.automod',     # Automod twelfth
            'cogs.dm_interaction',# DM interaction thirteenth
            'cogs.voice_channel',# Voice channel fourteenth
            'cogs.ocr',# OCR fifteenth
            'cogs.reddit',# Reddit sixteenth
            'cogs.interactions',# Interactions seventeenth
            'cogs.massrole'    # Mass role assignment eighteenth
        ]
        self.cog_status = {}

    async def setup_hook(self):
        logger.info('Starting bot setup...')
        
        # Load cogs with enhanced error handling
        for extension in self.initial_extensions:
            try:
                logger.debug(f'Attempting to load extension: {extension}')
                await self.load_extension(extension)
                self.cog_status[extension] = True
                logger.info(f'✓ Successfully loaded: {extension}')
            except Exception as e:
                self.cog_status[extension] = False
                logger.error(f'✗ Failed to load: {extension}')
                logger.error(f'Error type: {type(e).__name__}')
                logger.error(f'Error details: {str(e)}')
                logger.error(traceback.format_exc())
                continue

        # Sync commands with enhanced error handling
        try:
            logger.info('Syncing command tree...')
            synced = await self.tree.sync()
            logger.info(f'✓ Successfully synced {len(synced)} commands')
        except Exception as e:
            logger.error('✗ Failed to sync command tree')
            logger.error(f'Error type: {type(e).__name__}')
            logger.error(f'Error details: {str(e)}')
            logger.error(traceback.format_exc())

    async def on_ready(self):
        logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
        
        # Report cog status
        logger.info('\nCog Status:')
        for cog, status in self.cog_status.items():
            status_symbol = '✓' if status else '✗'
            logger.info(f'{status_symbol} {cog}')
        
        # Set activity
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{PREFIX}help | /help"
            )
        )
        logger.info('Bot is ready!')

bot = IndieGOBot()

async def main():
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Bot shutdown initiated by user')
    except Exception as e:
        logger.error(f'Unexpected error: {str(e)}')
        logger.error(traceback.format_exc())