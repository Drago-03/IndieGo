import discord
from discord.ext import commands
from discord import app_commands

class DMInteraction(commands.Cog):
    """Cog for handling DM interactions"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None and not message.author.bot:
            await message.channel.send("Hello! How can I assist you today?")

    @commands.command(name="update")
    async def update_command(self, ctx):
        """Send updates to users"""
        for member in ctx.guild.members:
            if not member.bot:
                try:
                    await member.send("Here are the latest updates...")
                except discord.Forbidden:
                    pass

async def setup(bot):
    await bot.add_cog(DMInteraction(bot))