import discord
from discord.ext import commands
from config import TOKEN, PREFIX
from discord import app_commands
import aiosqlite
import asyncio
import logging
import sys
import traceback

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

class IndieGOBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=PREFIX,
            intents=intents,
            help_command=None  # Disable default help command
        )
        self.initial_extensions = [
            'cogs.errors',  # Load error handler first
            'cogs.general',  # Load general first after errors
            'cogs.moderation',
            'cogs.fun',
            'cogs.admin',
            'cogs.tickets',
            'cogs.logging',
            'cogs.ai_assistant',
            'cogs.coding_help',
            'cogs.help',
            'cogs.base',
            'cogs.automod',
            'cogs.dm_interaction',
            'cogs.voice_channel',
            'cogs.ocr',
            'cogs.reddit'
        ]

    async def setup_hook(self):
        logger.info('Starting bot setup...')
        
        # Sync commands on startup
        try:
            synced = await self.tree.sync()
            logger.info(f'Synced {len(synced)} command(s)')
        except Exception as e:
            logger.error(f'Failed to sync commands: {str(e)}')
            logger.error(traceback.format_exc())
        
        # Load all cogs
        for extension in self.initial_extensions:
            try:
                await self.load_extension(extension)
                logger.info(f'Successfully loaded extension: {extension}')
            except Exception as e:
                logger.error(f'Failed to load extension {extension}: {str(e)}')
                logger.error(traceback.format_exc())

    async def on_ready(self):
        logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
        logger.info('------')

    async def on_command_error(self, ctx, error):
        # Pass all errors to the error handler cog
        if not hasattr(ctx.command, 'on_error'):
            return await ctx.cog.cog_command_error(ctx, error)

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