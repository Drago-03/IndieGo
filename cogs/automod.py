import discord
from discord.ext import commands
from discord import app_commands
import re

class AutoMod(commands.Cog):
    """Cog for advanced AutoMod features"""

    def __init__(self, bot):
        self.bot = bot
        self.bad_words = [
            # Add your bad words here
            # Example: "badword1", "badword2", etc.
        ]
        self.auto_mod_enabled = False

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if self.auto_mod_enabled and any(re.search(rf"\b{word}\b", message.content, re.IGNORECASE) for word in self.bad_words):
            await message.delete()
            await message.channel.send(f"{message.author.mention}, your message contained inappropriate content and was deleted.")
            await self.log_action(message.guild, f"Deleted message from {message.author} for inappropriate content.")

    async def log_action(self, guild, action):
        log_channel = discord.utils.get(guild.text_channels, name="mod-logs")
        if log_channel:
            await log_channel.send(action)

    @commands.command(name="warn")
    @commands.has_permissions(manage_messages=True)
    async def warn_command(self, ctx, member: discord.Member, *, reason: str):
        """Warn a member"""
        await member.send(f"You have been warned by {ctx.author}.\nReason: {reason}")
        await ctx.send(f"{member.mention} has been warned. Reason: {reason}")
        await self.log_action(ctx.guild, f"{ctx.author} warned {member}.\nReason: {reason}")

    @app_commands.command(name="warn", description="Warn a member")
    @app_commands.describe(member="The member to warn", reason="The reason for the warning")
    @commands.has_permissions(manage_messages=True)
    async def warn_slash(self, interaction: discord.Interaction, member: discord.Member, reason: str):
        """Warn a member"""
        await member.send(f"You have been warned by {interaction.user}.\nReason: {reason}")
        await interaction.response.send_message(f"{member.mention} has been warned. Reason: {reason}")
        await self.log_action(interaction.guild, f"{interaction.user} warned {member}.\nReason: {reason}")

    @commands.command(name="automod_setup")
    @commands.has_permissions(administrator=True)
    async def automod_setup_command(self, ctx):
        """Set up AutoMod in the server"""
        self.auto_mod_enabled = True
        await ctx.send("AutoMod has been enabled and set up for this server.")
        await self.log_action(ctx.guild, "AutoMod has been enabled and set up.")

    @app_commands.command(name="automod_setup", description="Set up AutoMod in the server")
    @commands.has_permissions(administrator=True)
    async def automod_setup_slash(self, interaction: discord.Interaction):
        """Set up AutoMod in the server"""
        self.auto_mod_enabled = True
        await interaction.response.send_message("AutoMod has been enabled and set up for this server.")
        await self.log_action(interaction.guild, "AutoMod has been enabled and set up.")

    @commands.command(name="add_bad_word")
    @commands.has_permissions(administrator=True)
    async def add_bad_word_command(self, ctx, *, word: str):
        """Add a bad word to the AutoMod filter"""
        self.bad_words.append(word)
        await ctx.send(f"Added '{word}' to the list of bad words.")
        await self.log_action(ctx.guild, f"Added '{word}' to the list of bad words.")

    @app_commands.command(name="add_bad_word", description="Add a bad word to the AutoMod filter")
    @commands.has_permissions(administrator=True)
    async def add_bad_word_slash(self, interaction: discord.Interaction, word: str):
        """Add a bad word to the AutoMod filter"""
        self.bad_words.append(word)
        await interaction.response.send_message(f"Added '{word}' to the list of bad words.")
        await self.log_action(interaction.guild, f"Added '{word}' to the list of bad words.")

    @commands.command(name="remove_bad_word")
    @commands.has_permissions(administrator=True)
    async def remove_bad_word_command(self, ctx, *, word: str):
        """Remove a bad word from the AutoMod filter"""
        if word in self.bad_words:
            self.bad_words.remove(word)
            await ctx.send(f"Removed '{word}' from the list of bad words.")
            await self.log_action(ctx.guild, f"Removed '{word}' from the list of bad words.")
        else:
            await ctx.send(f"'{word}' is not in the list of bad words.")

    @app_commands.command(name="remove_bad_word", description="Remove a bad word from the AutoMod filter")
    @commands.has_permissions(administrator=True)
    async def remove_bad_word_slash(self, interaction: discord.Interaction, word: str):
        """Remove a bad word from the AutoMod filter"""
        if word in self.bad_words:
            self.bad_words.remove(word)
            await interaction.response.send_message(f"Removed '{word}' from the list of bad words.")
            await self.log_action(interaction.guild, f"Removed '{word}' from the list of bad words.")
        else:
            await interaction.response.send_message(f"'{word}' is not in the list of bad words.")

async def setup(bot):
    await bot.add_cog(AutoMod(bot))