import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Select, View
import json

from config import INSTALL_URL

BOT_WEBSITE = "https://drago-03.github.io/IndieGo-Website/"
OWNER_ID = 950609706760691752 

class Help(commands.Cog):
    """Help and information commands"""

    def __init__(self, bot):
        self.bot = bot

    async def is_premium(self, user_id):
        # Check if the user has a premium subscription
        try:
            with open('premium_users.json', 'r') as f:
                premium_users = json.load(f)
            if user_id in premium_users:
                return premium_users[user_id]['tier']
        except FileNotFoundError:
            return None
        return None

    @commands.command(name="help")
    async def help_command(self, ctx):
        """Show help information with a dropdown menu"""
        embed = discord.Embed(
            title="IndieGO Bot Help",
            description="Select a category from the dropdown menu below to see the available commands.",
            color=discord.Color.blue()
        )
        view = HelpDropdownView(self.bot)
        await ctx.send(embed=embed, view=view)

    @app_commands.command(name="help", description="Show help information with a dropdown menu")
    async def help(self, interaction: discord.Interaction):
        """Show help information with a dropdown menu"""
        embed = discord.Embed(
            title="IndieGO Bot Help",
            description="Select a category from the dropdown menu below to see the available commands.",
            color=discord.Color.blue()
        )
        view = HelpDropdownView(self.bot)
        await interaction.response.send_message(embed=embed, view=view)

    @commands.command(name="serverinfo")
    async def serverinfo_command(self, ctx):
        """Show information about the server"""
        guild = ctx.guild
        embed = discord.Embed(
            title=f"Server Info - {guild.name}",
            description=f"Information about the server {guild.name}",
            color=discord.Color.blue()
        )
        embed.add_field(name="Server ID", value=guild.id, inline=False)
        embed.add_field(name="Owner", value=guild.owner, inline=False)
        embed.add_field(name="Region", value=guild.region, inline=False)
        embed.add_field(name="Members", value=guild.member_count, inline=False)
        embed.add_field(name="Created At", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        await ctx.send(embed=embed)

    @app_commands.command(name="serverinfo", description="Show information about the server")
    async def serverinfo(self, interaction: discord.Interaction):
        """Show information about the server"""
        guild = interaction.guild
        embed = discord.Embed(
            title=f"Server Info - {guild.name}",
            description=f"Information about the server {guild.name}",
            color=discord.Color.blue()
        )
        embed.add_field(name="Server ID", value=guild.id, inline=False)
        embed.add_field(name="Owner", value=guild.owner, inline=False)
        embed.add_field(name="Region", value=guild.region, inline=False)
        embed.add_field(name="Members", value=guild.member_count, inline=False)
        embed.add_field(name="Created At", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        await interaction.response.send_message(embed=embed)

class HelpDropdownView(View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.add_item(HelpDropdown(bot))

class HelpDropdown(Select):
    def __init__(self, bot):
        self.bot = bot
        options = [
            discord.SelectOption(label="Programming", description="Commands related to programming help"),
            discord.SelectOption(label="Moderation", description="Commands for server moderation"),
            discord.SelectOption(label="Fun", description="Fun commands"),
            discord.SelectOption(label="Admin", description="Administrative commands"),
            discord.SelectOption(label="Tickets", description="Ticket management commands"),
            discord.SelectOption(label="AI-Developer Assistance", description="AI-powered developer assistance commands"),
            discord.SelectOption(label="Voice Channel", description="Voice channel features"),
            discord.SelectOption(label="OCR", description="OCR and image scanning"),
            discord.SelectOption(label="Reddit", description="Reddit integration"),
            discord.SelectOption(label="AutoMod", description="Advanced AutoMod features"),
            discord.SelectOption(label="DM Interaction", description="Interact with the bot via DMs"),
            discord.SelectOption(label="Logging", description="Log actions and errors")
        ]
        super().__init__(placeholder="Choose a category...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        category = self.values[0]
        embed = discord.Embed(
            title=f"{category} Commands",
            description=f"Here are the commands available in the {category} category:",
            color=discord.Color.blue()
        )
        if category == "Programming":
            embed.add_field(
                name="Commands",
                value="code - Get coding help\n"
                      "explain - Explain code in simple terms\n"
                      "debug - Help debug code issues\n"
                      "optimize - Suggest code optimizations\n"
                      "scan_image - Scan an image for code and provide help",
                inline=False
            )
        elif category == "Moderation":
            embed.add_field(
                name="Commands",
                value="kick - Kick a member\n"
                      "ban - Ban a member\n"
                      "unban - Unban a member\n"
                      "mute - Mute a member\n"
                      "unmute - Unmute a member\n"
                      "timeout - Temporarily mute a member\n"
                      "warn - Warn a member\n"
                      "clear - Clear messages",
                inline=False
            )
        elif category == "Fun":
            embed.add_field(
                name="Commands",
                value="roll - Roll a dice\n"
                      "choose - Choose between multiple choices\n"
                      "poll - Create a poll\n"
                      "trivia - Start a trivia game\n"
                      "codechallenge - Get a random coding challenge\n"
                      "quote - Get a random inspirational quote\n"
                      "joke - Get a random programming joke",
                inline=False
            )
        elif category == "Admin":
            embed.add_field(
                name="Commands",
                value="load - Load a cog\n"
                      "unload - Unload a cog\n"
                      "reload - Reload a cog\n"
                      "setstatus - Set the bot's status\n"
                      "announce - Send an announcement\n"
                      "shutdown - Shut down the bot\n"
                      "gift - Gift a premium tier\n"
                      "team - Add a team member\n"
                      "about - Show information about the bot\n"
                      "ping - Check the bot's latency",
                inline=False
            )
        elif category == "Tickets":
            embed.add_field(
                name="Commands",
                value="ticket - Create a ticket\n"
                      "setup_logs - Setup logging channels",
                inline=False
            )
        elif category == "AI-Developer Assistance":
            embed.add_field(
                name="Commands",
                value="ask - Ask a general question to the AI assistant\n"
                      "codehelp - Get coding help using multiple AI models",
                inline=False
            )
        elif category == "Voice Channel":
            embed.add_field(
                name="Commands",
                value="join - Join a voice channel\n"
                      "leave - Leave a voice channel\n"
                      "play - Play a sound from a URL\n"
                      "record - Record voice and convert to text",
                inline=False
            )
        elif category == "OCR":
            embed.add_field(
                name="Commands",
                value="scan - Scan an image for text",
                inline=False
            )
        elif category == "Reddit":
            embed.add_field(
                name="Commands",
                value="meme - Fetch a programming meme from Reddit",
                inline=False
            )
        elif category == "AutoMod":
            embed.add_field(
                name="Commands",
                value="warn - Warn a member",
                inline=False
            )
        elif category == "DM Interaction":
            embed.add_field(
                name="Commands",
                value="update - Send updates to users",
                inline=False
            )
        elif category == "Logging":
            embed.add_field(
                name="Commands",
                value="initialize_logs - Setup logging channels",
                inline=False
            )
        await interaction.response.edit_message(embed=embed, view=self.view)

async def setup(bot):
    await bot.add_cog(Help(bot))