import discord
from discord.ext import commands
import os
from config import DISCORD_BOT_TOKEN, validate_discord_keys

class IndieGOBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix='!', intents=intents)
        
        # Define initial extensions here
        self.initial_extensions = [
            'cogs.general',
            'cogs.tickets',
            'cogs.admin'
        ]

    async def setup_hook(self):
        # Load extensions
        for extension in self.initial_extensions:
            try:
                await self.load_extension(extension)
            except Exception as e:
                print(f'Failed to load extension {extension}: {e}')

    async def on_ready(self):
        print(f'Logged in as {self.user.name}')
        print('------')

def main():
    try:
        # Validate all required keys before starting
        validate_discord_keys()
        
        # Create and start the bot
        bot = IndieGOBot()
        bot.run(DISCORD_BOT_TOKEN)
    except ValueError as e:
        print(f"Configuration Error: {e}")
        exit(1)
    except Exception as e:
        print(f"Startup Error: {e}")
        exit(1)

if __name__ == '__main__':
    main() 