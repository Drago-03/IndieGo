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
            channel = discord.utils.get(guild.text_channels, name=name)
            if not channel:
                channel = await guild.create_text_channel(name, category=self.log_category)
            self.log_channels[name] = channel

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

    @app_commands.command(name="log", description="Log a message")
    async def log(self, interaction: discord.Interaction, log_type: str, message: str):
        if not await self.is_premium(interaction.user.id):
            await interaction.response.send_message("This is a premium feature. Please subscribe to access it.", ephemeral=True)
            return

        if log_type not in self.log_channels:
            await interaction.response.send_message("Invalid log type.", ephemeral=True)
            return

        embed = discord.Embed(title="Log Entry", description=message, color=discord.Color.blue())
        embed.set_footer(text=f"Logged by {interaction.user}", icon_url=interaction.user.avatar.url)
        await self.log_channels[log_type].send(embed=embed)
        await interaction.response.send_message("Log entry created.", ephemeral=True)

    @app_commands.command(name="setup_logs", description="Setup logging channels")
    async def setup_logs(self, interaction: discord.Interaction):
        if not await self.is_premium(interaction.user.id):
            await interaction.response.send_message("This is a premium feature. Please subscribe to access it.", ephemeral=True)
            return

        guild = interaction.guild
        self.log_category = discord.utils.get(guild.categories, name="Logs")
        if not self.log_category:
            self.log_category = await guild.create_category("Logs")

        log_channel_names = ["general-logs", "error-logs", "command-logs"]
        for name in log_channel_names:
            channel = discord.utils.get(guild.text_channels, name=name)
            if not channel:
                channel = await guild.create_text_channel(name, category=self.log_category)
            self.log_channels[name] = channel

        await interaction.response.send_message("Logging channels setup completed.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Logging(bot))