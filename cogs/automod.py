import discord
from discord.ext import commands
import re

class AutoMod(commands.Cog):
    """Cog for advanced AutoMod features"""

    def __init__(self, bot):
        self.bot = bot
        self.bad_words = ["badword1", "badword2"]  # Add more bad words here

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if any(re.search(rf"\b{word}\b", message.content, re.IGNORECASE) for word in self.bad_words):
            await message.delete()
            await message.channel.send(f"{message.author.mention}, your message contained inappropriate content and was deleted.")
            await self.log_action(message.guild, f"Deleted message from {message.author} for inappropriate content.")

    async def log_action(self, guild, action):
        log_channel = discord.utils.get(guild.text_channels, name="mod-logs")
        if log_channel:
            await log_channel.send(action)

    @commands.command(name="warn")
    async def warn_command(self, ctx, member: discord.Member, *, reason: str):
        """Warn a member"""
        await member.send(f"You have been warned by {ctx.author}.\nReason: {reason}")
        await ctx.send(f"{member.mention} has been warned. Reason: {reason}")
        await self.log_action(ctx.guild, f"{ctx.author} warned {member}.\nReason: {reason}")

async def setup(bot):
    await bot.add_cog(AutoMod(bot))