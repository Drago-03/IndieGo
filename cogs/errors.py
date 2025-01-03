import discord
from discord.ext import commands
import traceback

class ErrorHandler(commands.Cog):
    """Cog for handling errors and displaying them professionally"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        log_channel_id = 1313272659026514050
        log_channel = self.bot.get_channel(log_channel_id)

        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="⚠️ Missing Required Argument",
                description=f"**Error:** The command `{ctx.command}` requires additional information.\n\n"
                          f"**Details:** Missing parameter: `{error.param.name}`\n\n"
                          f"**Example Usage:**\n```\n{ctx.prefix}{ctx.command.qualified_name} {ctx.command.signature}\n```",
                color=discord.Color.gold()
            )

        elif isinstance(error, commands.CommandNotFound):
            command_name = ctx.message.content.split()[0][1:]  # Remove prefix
            embed = discord.Embed(
                title="❌ Command Not Found",
                description=f"**Error:** The command `{command_name}` does not exist.\n\n"
                          f"**Solution:** Use `{ctx.prefix}help` to see all available commands.\n\n"
                          f"**Note:** Commands are case-sensitive.",
                color=discord.Color.red()
            )

        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="🔒 Missing Permissions",
                description=f"**Error:** You lack the required permissions.\n\n"
                          f"**Required Permissions:**\n```\n{', '.join(error.missing_permissions)}\n```\n"
                          f"**Note:** Contact a server administrator if you believe this is a mistake.",
                color=discord.Color.red()
            )

        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                title="🤖 Bot Missing Permissions",
                description=f"**Error:** I don't have the required permissions.\n\n"
                          f"**Required Permissions:**\n```\n{', '.join(error.missing_permissions)}\n```\n"
                          f"**Solution:** Ask a server administrator to grant me these permissions.",
                color=discord.Color.red()
            )

        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="⏳ Command on Cooldown",
                description=f"**Error:** This command is on cooldown.\n\n"
                          f"**Time Remaining:** {error.retry_after:.1f} seconds\n\n"
                          f"**Note:** This limit helps prevent spam and ensures fair usage.",
                color=discord.Color.blue()
            )

        else:
            error_traceback = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
            embed = discord.Embed(
                title="⚠️ Unexpected Error",
                description=f"**Error Type:** `{type(error).__name__}`\n\n"
                          f"**Details:**\n```py\n{str(error)}\n```\n\n"
                          f"**Developer Info:**\n```py\n{error_traceback[:1000]}\n```",
                color=discord.Color.red()
            )

        # Add common footer
        embed.set_footer(text=f"Command: {ctx.prefix}{ctx.command if ctx.command else 'Unknown'}")

        # Send error to user
        await ctx.send(embed=embed)

        # Log error
        if log_channel:
            log_embed = discord.Embed(
                title="🔍 Error Log Entry",
                description=f"Error occurred in {ctx.guild.name}",
                color=discord.Color.red()
            )
            log_embed.add_field(name="User", value=f"{ctx.author} ({ctx.author.id})", inline=True)
            log_embed.add_field(name="Channel", value=f"{ctx.channel.name} ({ctx.channel.id})", inline=True)
            log_embed.add_field(name="Command", value=f"{ctx.message.content[:1000]}", inline=False)
            log_embed.add_field(name="Error", value=f"```py\n{error_traceback[:1000]}\n```", inline=False)
            await log_channel.send(embed=log_embed)

async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))