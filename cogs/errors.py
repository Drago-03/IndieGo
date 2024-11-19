import discord
from discord.ext import commands

class ErrorHandler(commands.Cog):
    """Cog for handling errors and displaying them professionally"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="Missing Required Argument",
                description=f"You're missing a required argument: `{error.param.name}`.\nPlease provide all required arguments and try again.",
                color=discord.Color.red()
            )
        elif isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(
                title="Command Not Found",
                description="The command you tried to use does not exist. Please check the command and try again.",
                color=discord.Color.red()
            )
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="Missing Permissions",
                description="You do not have the required permissions to use this command.",
                color=discord.Color.red()
            )
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                title="Bot Missing Permissions",
                description="I do not have the required permissions to execute this command.",
                color=discord.Color.red()
            )
        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="Command On Cooldown",
                description=f"This command is on cooldown. Please try again after {error.retry_after:.2f} seconds.",
                color=discord.Color.red()
            )
        else:
            embed = discord.Embed(
                title="An Error Occurred",
                description="An unexpected error occurred. Please try again later.",
                color=discord.Color.red()
            )
            embed.add_field(name="Error Details", value=str(error))

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))