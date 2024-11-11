import discord
from discord.ext import commands
from .base import BaseCog
from config import INSTALL_URL, BOT_WEBSITE

class Help(BaseCog):
    """Help and information commands"""

    @commands.command()
    async def help(self, ctx):
        """Show help information"""
        embed = self.create_embed(
            "DevAssist Bot Help",
            "Your AI-powered coding assistant!"
        )

        # Add command categories
        embed.add_field(
            name="🔧 Programming",
            value="`!code` - Get coding help\n"
                  "`!review` - Code review\n"
                  "`!explain` - Explain code",
            inline=False
        )

        embed.add_field(
            name="🎫 Support",
            value="`!ticket` - Create support ticket\n"
                  "`!close` - Close ticket",
            inline=False
        )

        embed.add_field(
            name="🎮 Fun",
            value="`!roll` - Roll dice\n"
                  "`!joke` - Programming joke\n"
                  "`!poll` - Create poll",
            inline=False
        )

        # Add links
        embed.add_field(
            name="📚 Resources",
            value=f"[Website]({BOT_WEBSITE}) | "
                  f"[Add to Server]({INSTALL_URL}) | "
                  "[Support Server](https://discord.gg/your-invite)",
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def about(self, ctx):
        """Show information about the bot"""
        embed = self.create_embed(
            "About DevAssist",
            "The ultimate Discord bot for developer communities!"
        )

        embed.add_field(
            name="🌟 Features",
            value="• AI-powered code assistance\n"
                  "• Project management\n"
                  "• Support ticket system\n"
                  "• Fun developer utilities",
            inline=False
        )

        embed.add_field(
            name="🔗 Links",
            value=f"[Website]({BOT_WEBSITE})\n"
                  f"[Add to Server]({INSTALL_URL})\n"
                  "[Support Server](https://discord.gg/your-invite)\n"
                  "[GitHub](https://github.com/your-username/devassist-bot)",
            inline=False
        )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))