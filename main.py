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
        super().__init__(
            command_prefix=PREFIX, 
            intents=intents,
            help_command=None  # Disable default help command
        )
        self.initial_extensions = [
            'cogs.general',
            'cogs.moderation',
            'cogs.fun',
            'cogs.admin',
            'cogs.tickets',
            'cogs.logging',
            'cogs.ai_assistant',
            'cogs.coding_help',
            'cogs.help',  # Load help cog last
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
        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")
        logger.info("------")

    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if commands.Cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        logger.error('Ignoring exception in command {}:'.format(ctx.command), exc_info=error)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

bot = IndieGOBot()

async def main():
    async with bot:
        await bot.start(TOKEN)

asyncio.run(main())