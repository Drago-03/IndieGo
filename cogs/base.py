import discord
from discord.ext import commands
from config import EMBED_COLOR, AUTHOR_NAME, AUTHOR_ICON

class BaseCog(commands.Cog):
    """Base cog with shared utilities"""
    
    def __init__(self, bot):
        self.bot = bot

    def create_embed(self, title: str, description: str = None) -> discord.Embed:
        """Create a branded embed"""
        embed = discord.Embed(
            title=title,
            description=description,
            color=EMBED_COLOR
        )
        embed.set_footer(
            text=AUTHOR_NAME,
            icon_url=AUTHOR_ICON
        )
        return embed

    async def send_error(self, ctx, message: str):
        """Send an error message"""
        embed = self.create_embed("Error ❌", message)
        await ctx.send(embed=embed)

    async def send_success(self, ctx, message: str):
        """Send a success message"""
        embed = self.create_embed("Success ✅", message)
        await ctx.send(embed=embed)