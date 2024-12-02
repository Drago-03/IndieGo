import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Select, View

from config import SUPPORT_SERVER_LINK

class HelpDropdown(Select):
    def __init__(self, bot):
        self.bot = bot
        options = [
            discord.SelectOption(label="General", description="General bot commands", emoji="🤖"),
            discord.SelectOption(label="Moderation", description="Moderation commands", emoji="🛡️"),
            discord.SelectOption(label="Fun", description="Fun commands", emoji="🎮"),
            discord.SelectOption(label="AI Assistant", description="AI-powered commands", emoji="🤖"),
            discord.SelectOption(label="Coding", description="Programming help commands", emoji="💻"),
            discord.SelectOption(label="Reddit", description="Reddit commands", emoji="🔗"),
            discord.SelectOption(label="AutoMod", description="AutoMod commands", emoji="🔒"),
            discord.SelectOption(label="DM Interaction", description="DM interaction commands", emoji="✉️"),
            discord.SelectOption(label="Logging", description="Logging commands", emoji="📜"),
            discord.SelectOption(label="Tickets", description="Ticketing commands", emoji="🎫"),
            discord.SelectOption(label="Voice", description="Voice channel commands", emoji="🔊"),
            discord.SelectOption(label="OCR", description="OCR commands", emoji="📄")
        ]
        super().__init__(placeholder="Choose a category...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        category = self.values[0]
        embed = discord.Embed(title=f"{category} Commands", description=f"Here are the commands for {category}:", color=discord.Color.blue())
        
        if category == "General":
            embed.add_field(name="Commands", value="• ping - Check bot latency\n• about - About the bot\n• choose - Choose between options\n• serverinfo - Server information\n• support - Get the link to the support server\n• profile - Show profile options for the user", inline=False)
        elif category == "Moderation":
            embed.add_field(name="Commands", value="• kick - Kick a member\n• ban - Ban a member\n• mute - Mute a member\n• unmute - Unmute a member\n• warn - Warn a member", inline=False)
        elif category == "Fun":
            embed.add_field(name="Commands", value="• roll - Roll a dice\n• 8ball - Ask the magic 8ball\n• joke - Get a random joke\n• codechallenge - Gives a random coding challenge\n• trivia - Starts a trivia game with programming questions", inline=False)
        elif category == "AI Assistant":
            embed.add_field(name="Commands", value="• ask - Ask the AI a question\n• codehelp - Get coding help", inline=False)
        elif category == "Coding":
            embed.add_field(name="Commands", value="• debug - Debug your code\n• optimize - Optimize your code", inline=False)
        elif category == "Reddit":
            embed.add_field(name="Commands", value="• meme - Fetch a programming meme from Reddit", inline=False)
        elif category == "AutoMod":
            embed.add_field(name="Commands", value="• warn - Warn a member\n• automod_setup - Set up AutoMod\n• add_bad_word - Add a bad word\n• remove_bad_word - Remove a bad word", inline=False)
        elif category == "DM Interaction":
            embed.add_field(name="Commands", value="• update - Send updates to users", inline=False)
        elif category == "Logging":
            embed.add_field(name="Commands", value="• setup_logs - Setup logging channels", inline=False)
        elif category == "Tickets":
            embed.add_field(name="Commands", value="• ticket - Create a ticket\n• setup_tickets - Setup ticketing system", inline=False)
        elif category == "Voice":
            embed.add_field(name="Commands", value="• join - Join a voice channel\n• leave - Leave a voice channel", inline=False)
        elif category == "OCR":
            embed.add_field(name="Commands", value="• scan - Scan an image for text", inline=False)
        
        await interaction.response.edit_message(embed=embed, view=self.view)

class HelpView(View):
    def __init__(self, bot):
        super().__init__(timeout=60)
        self.add_item(HelpDropdown(bot))

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        """Show help information with a dropdown menu"""
        embed = discord.Embed(
            title="IndieGO Bot Help",
            description="Select a category from the dropdown menu below to see the available commands.",
            color=discord.Color.blue()
        )
        view = HelpView(self.bot)
        await ctx.send(embed=embed, view=view)

    @app_commands.command(name="help", description="Show help information with a dropdown menu")
    async def help_slash(self, interaction: discord.Interaction):
        """Show help information with a dropdown menu"""
        embed = discord.Embed(
            title="IndieGO Bot Help",
            description="Select a category from the dropdown menu below to see the available commands.",
            color=discord.Color.blue()
        )
        view = HelpView(self.bot)
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

    @commands.command(name="support")
    async def support_command(self, ctx):
        """Get the link to the support server"""
        embed = discord.Embed(
            title="Support Server",
            description=f"If you need help or have any questions, join our support server: [Support Server]({SUPPORT_SERVER_LINK})",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @app_commands.command(name="support", description="Get the link to the support server")
    async def support(self, interaction: discord.Interaction):
        """Get the link to the support server"""
        embed = discord.Embed(
            title="Support Server",
            description=f"If you need help or have any questions, join our support server: [Support Server]({SUPPORT_SERVER_LINK})",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))