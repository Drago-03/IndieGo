import discord
from discord.ext import commands
from config import EMBED_COLOR, AUTHOR_NAME, AUTHOR_ICON

class BaseCog(commands.Cog):
    """Base cog with shared utilities"""
    
    def __init__(self, bot):
        self.bot = bot

    def create_embed(self, title: str, description: str = None, error: bool = False) -> discord.Embed:
        """Create a branded embed"""
        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.red() if error else EMBED_COLOR
        )
        embed.set_footer(
            text=AUTHOR_NAME,
            icon_url=AUTHOR_ICON
        )
        return embed

    async def send_error(self, ctx, message: str):
        """Send a professionally formatted error message"""
        embed = self.create_embed(
            "⚠️ An Error Occurred",
            f"I apologize, but {message.lower()}. Please try again or contact support if this persists.",
            error=True
        )
        await ctx.send(embed=embed)

    async def send_cooldown_error(self, ctx, retry_after: float):
        """Send a cooldown error message"""
        embed = self.create_embed(
            "⏳ Command on Cooldown",
            f"This command is currently on cooldown. Please try again in {retry_after:.1f} seconds.",
            error=True
        )
        await ctx.send(embed=embed)

    async def send_permission_error(self, ctx):
        """Send a permission error message"""
        embed = self.create_embed(
            "🔒 Permission Required",
            "You don't have the required permissions to use this command. Please contact a server administrator.",
            error=True
        )
        await ctx.send(embed=embed)

    async def send_success(self, ctx, message: str):
        """Send a success message"""
        embed = self.create_embed("✅ Success", message)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(BaseCog(bot))