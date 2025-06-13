import asyncio
import logging
import sys
import traceback
import discord
from discord.ext import commands
import os
from config import TOKEN, PREFIX, LOG_CHANNEL_ID

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,  # Change to DEBUG for more info
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('IndieGOBot')

# Define test guild IDs for faster command registration during development
TEST_GUILD_IDS = [1308525132620914688]  # Test server ID

# Set up intents
intents = discord.Intents.all()  # Use all intents for testing

class SimpleBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or(PREFIX),  # Respond to mentions too
            intents=intents,
            description="A Discord bot for developers",
            case_insensitive=True,
            help_command=None
        )
        
    async def setup_hook(self):
        logger.info('Bot setup starting...')
        
        # Add basic commands directly
        self.add_commands()
        
        # Try to load the general cog
        try:
            await self.load_extension('cogs.general')
            logger.info('✓ Successfully loaded general cog')
        except Exception as e:
            logger.error(f'✗ Failed to load general cog: {str(e)}')
            logger.error(traceback.format_exc())
        
        # Sync commands
        try:
            logger.info('Syncing commands...')
            for guild_id in TEST_GUILD_IDS:
                try:
                    # Copy commands to guild for immediate testing
                    self.tree.copy_global_to(guild=discord.Object(id=guild_id))
                    await self.tree.sync(guild=discord.Object(id=guild_id))
                    logger.info(f'✓ Synced commands to guild {guild_id}')
                except Exception as e:
                    logger.error(f'✗ Failed to sync guild commands: {str(e)}')
            
            # Sync globally
            await self.tree.sync()
            logger.info('✓ Synced global commands')
        except Exception as e:
            logger.error(f'✗ Failed to sync commands: {str(e)}')
            logger.error(traceback.format_exc())
    
    def add_commands(self):
        """Add basic commands directly to the bot"""
        
        # Basic ping command
        @self.command(name="ping")
        async def ping(ctx):
            await ctx.send(f"🏓 Pong! Bot latency: {round(self.latency * 1000)}ms")
        
        # Basic about command
        @self.command(name="about")
        async def about(ctx):
            embed = discord.Embed(
                title="🤖 About IndieGO Bot",
                description="Your Ultimate Development & Design Companion",
                color=discord.Color.blue()
            )
            embed.add_field(name="Version", value="1.0.0", inline=True)
            embed.add_field(name="Library", value=f"Discord.py {discord.__version__}", inline=True)
            await ctx.send(embed=embed)
        
        # Basic test command
        @self.command(name="test")
        async def test(ctx):
            await ctx.send("✅ Bot is working! This is a test command.")
        
        # Basic sync command
        @self.command(name="sync")
        @commands.is_owner()
        async def sync_cmd(ctx):
            await ctx.send("Syncing commands...")
            try:
                # Sync to test guild
                for guild_id in TEST_GUILD_IDS:
                    self.tree.copy_global_to(guild=discord.Object(id=guild_id))
                    await self.tree.sync(guild=discord.Object(id=guild_id))
                
                # Sync globally
                synced = await self.tree.sync()
                await ctx.send(f"✅ Synced {len(synced)} commands globally")
            except Exception as e:
                await ctx.send(f"❌ Error: {str(e)}")
        
        # Add slash commands
        @self.tree.command(name="ping", description="Check bot latency")
        async def ping_slash(interaction: discord.Interaction):
            await interaction.response.send_message(
                f"🏓 Pong! Bot latency: {round(self.latency * 1000)}ms"
            )
        
        @self.tree.command(name="about", description="About the bot")
        async def about_slash(interaction: discord.Interaction):
            embed = discord.Embed(
                title="🤖 About IndieGO Bot",
                description="Your Ultimate Development & Design Companion",
                color=discord.Color.blue()
            )
            embed.add_field(name="Version", value="1.0.0", inline=True)
            embed.add_field(name="Library", value=f"Discord.py {discord.__version__}", inline=True)
            await interaction.response.send_message(embed=embed)
        
        logger.info("✓ Added basic commands to bot")
    
    async def on_ready(self):
        logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
        
        # Set activity
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name=f"{PREFIX}help | /help"
            )
        )
        
        # Print available commands for debugging
        logger.info("\nAvailable Commands:")
        for command in self.commands:
            logger.info(f"Prefix Command: {command.name}")
        
        slash_commands = self.tree.get_commands()
        for command in slash_commands:
            logger.info(f"Slash Command: {command.name}")
        
        logger.info('Bot is ready!')

    async def on_command_error(self, ctx, error):
        """Handle command errors"""
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f"❌ Command not found. Try `{PREFIX}help` to see available commands.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"❌ Missing required argument: {error.param.name}")
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"❌ Bad argument: {str(error)}")
        else:
            logger.error(f"Command error: {str(error)}")
            await ctx.send(f"❌ An error occurred: {str(error)}")

# Create bot instance
bot = SimpleBot()

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