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

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Handle errors globally"""
        if isinstance(error, commands.MissingPermissions):
            await self.send_permission_error(ctx)
        elif isinstance(error, commands.CommandOnCooldown):
            await self.send_cooldown_error(ctx, error.retry_after)
        elif isinstance(error, commands.MissingRequiredArgument):
            await self.send_error(ctx, f"you're missing a required argument: {error.param.name}")
        elif isinstance(error, commands.CommandNotFound):
            await self.send_error(ctx, "the command you tried to use does not exist")
        else:
            await self.send_error(ctx, "an unexpected error occurred")

    @commands.Cog.listener()
    async def on_message(self, message):
        """Handle messages to check for unauthorized command usage"""
        if message.author.bot:
            return

        if any(role.permissions.administrator for role in message.author.roles):
            return

        if any(command in message.content for command in ["!kick", "!ban", "!mute", "!warn"]):
            await message.channel.send(f"{message.author.mention}, you don't have permission to use moderation commands.")

async def setup(bot):
    await bot.add_cog(BaseCog(bot))