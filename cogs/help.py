import discord
from discord.ext import commands
from discord import app_commands
import json

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

    @app_commands.command(name="help", description="Show help information")
    async def help(self, interaction: discord.Interaction):
        """Show help information"""
        embed = discord.Embed(
            title="IndieGO Bot Help",
            description="Here are my available commands:",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="Programming",
            value="/code - Get coding help\n"
                  "/explain - Explain code in simple terms\n"
                  "/debug - Help debug code issues\n"
                  "/optimize - Suggest code optimizations\n"
                  "/scan_image - Scan an image for code and provide help",
            inline=False
        )
        embed.add_field(
            name="Moderation",
            value="/kick - Kick a member\n"
                  "/ban - Ban a member\n"
                  "/unban - Unban a member\n"
                  "/mute - Mute a member\n"
                  "/unmute - Unmute a member\n"
                  "/timeout - Temporarily mute a member\n"
                  "/warn - Warn a member\n"
                  "/clear - Clear messages",
            inline=False
        )
        embed.add_field(
            name="Fun",
            value="/roll - Roll a dice\n"
                  "/choose - Choose between multiple choices\n"
                  "/poll - Create a poll\n"
                  "/trivia - Start a trivia game\n"
                  "/codechallenge - Get a random coding challenge\n"
                  "/quote - Get a random inspirational quote\n"
                  "/joke - Get a random programming joke",
            inline=False
        )
        embed.add_field(
            name="Admin",
            value="/load - Load a cog\n"
                  "/unload - Unload a cog\n"
                  "/reload - Reload a cog\n"
                  "/setstatus - Set the bot's status\n"
                  "/announce - Send an announcement\n"
                  "/shutdown - Shut down the bot\n"
                  "/gift - Gift a premium tier\n"
                  "/team - Add a team member\n"
                  "/about - Show information about the bot\n"
                  "/ping - Check the bot's latency",
            inline=False
        )
        embed.add_field(
            name="Tickets",
            value="/ticket - Create a ticket\n"
                  "/setup_logs - Setup logging channels",
            inline=False
        )
        embed.add_field(
            name="Subscription Tiers",
            value="**Free Tier**\n"
                  "- Code review with security analysis\n"
                  "- Basic ticket system\n"
                  "- Programming assistance\n"
                  "- Fun developer utilities\n\n"
                  "**Pro Tier ($9.99/month)**\n"
                  "- Advanced code analysis\n"
                  "- Performance optimization\n"
                  "- Project templates\n"
                  "- GitHub integration\n"
                  "- Custom commands\n"
                  "- Advanced logging\n\n"
                  "**Team Tier ($19.99/month)**\n"
                  "- All Pro features\n"
                  "- Team management\n"
                  "- Custom ticket categories\n"
                  "- Custom ticket forms\n\n"
                  "**Enterprise Tier ($29.99/month)**\n"
                  "- All Team features\n"
                  "- Dedicated support\n"
                  "- Custom integrations\n"
                  "- SLA guarantees",
            inline=False
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="about", description="Show information about the bot")
    async def about(self, interaction: discord.Interaction):
        """Show information about the bot"""
        embed = discord.Embed(
            title="About IndieGO Bot",
            description="The ultimate Discord bot for developer communities!",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="Creator",
            value="Drago (drago.exe)",
            inline=False
        )
        embed.add_field(
            name="Support Server",
            value="[Support Server](https://discord.gg/your-invite)",
            inline=False
        )
        embed.add_field(
            name="Links",
            value=f"[Website]({BOT_WEBSITE})\n"
                  f"[Add to Server]({INSTALL_URL})\n"
                  "[GitHub](https://github.com/your-username/devassist-bot)",
            inline=False
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))