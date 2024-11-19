import discord
from discord.ext import commands
from discord import app_commands
import json

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_category = None
        self.log_channels = {}

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.guilds[0]
        self.log_category = discord.utils.get(guild.categories, name="Logs")
        if not self.log_category:
            self.log_category = await guild.create_category("Logs")

        log_channel_names = ["general-logs", "error-logs", "command-logs"]
        for name in log_channel_names:
            try:
                channel = discord.utils.get(guild.text_channels, name=name)
                if not channel:
                    channel = await guild.create_text_channel(name, category=self.log_category)
                self.log_channels[name] = channel
            except Exception as e:
                print(f"Failed to create or get channel {name}: {e}")

    async def is_premium(self, user_id):
        # Check if the user has a premium subscription
        try:
            with open('premium_users.json', 'r') as f:
                premium_users = json.load(f)
            if user_id in premium_users:
                return True
        except FileNotFoundError:
            return False
        return False

    @commands.command(name="initialize_logs")
    async def initialize_logs_command(self, ctx):
        """Setup logging channels"""
        guild = ctx.guild
        self.log_category = discord.utils.get(guild.categories, name="Logs")
        if not self.log_category:
            self.log_category = await guild.create_category("Logs")

        log_channel_names = ["general-logs", "error-logs", "command-logs"]
        for name in log_channel_names:
            try:
                channel = discord.utils.get(guild.text_channels, name=name)
                if not channel:
                    channel = await guild.create_text_channel(name, category=self.log_category)
                self.log_channels[name] = channel
            except Exception as e:
                await ctx.send(f"Failed to create or get channel {name}: {e}")
                return

        await ctx.send("Logging channels setup successfully.")

    @app_commands.command(name="initialize_logs", description="Setup logging channels")
    async def initialize_logs(self, interaction: discord.Interaction):
        """Setup logging channels"""
        guild = interaction.guild
        self.log_category = discord.utils.get(guild.categories, name="Logs")
        if not self.log_category:
            self.log_category = await guild.create_category("Logs")

        log_channel_names = ["general-logs", "error-logs", "command-logs"]
        for name in log_channel_names:
            try:
                channel = discord.utils.get(guild.text_channels, name=name)
                if not channel:
                    channel = await guild.create_text_channel(name, category=self.log_category)
                self.log_channels[name] = channel
            except Exception as e:
                await interaction.response.send_message(f"Failed to create or get channel {name}: {e}", ephemeral=True)
                return

        await interaction.response.send_message("Logging channels setup successfully.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Logging(bot))