import discord
from discord.ext import commands

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
                title="Missing Required Argument",
                description=f"You're missing a required argument: `{error.param.name}`.\nPlease provide all required arguments and try again.",
                color=discord.Color.red()
            )
            user_message = "You're missing a required argument. Please check the command and try again."
        elif isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(
                title="Command Not Found",
                description="The command you tried to use does not exist. Please check the command and try again.",
                color=discord.Color.red()
            )
            user_message = "The command you tried to use does not exist. Please check the command and try again."
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="Missing Permissions",
                description="You do not have the required permissions to use this command.",
                color=discord.Color.red()
            )
            user_message = "You do not have the required permissions to use this command."
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                title="Bot Missing Permissions",
                description="I do not have the required permissions to execute this command.",
                color=discord.Color.red()
            )
            user_message = "I do not have the required permissions to execute this command."
        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="Command On Cooldown",
                description=f"This command is on cooldown. Please try again after {error.retry_after:.2f} seconds.",
                color=discord.Color.red()
            )
            user_message = f"This command is on cooldown. Please try again after {error.retry_after:.2f} seconds."
        else:
            embed = discord.Embed(
                title="An Error Occurred",
                description="An unexpected error occurred. Please try again later.",
                color=discord.Color.red()
            )
            embed.add_field(name="Error Details", value=str(error))
            user_message = "An unexpected error occurred. Please try again later."

        # Send the error message to the user
        await ctx.send(embed=embed)

        # Log the error in the specified log channel
        if log_channel:
            log_embed = discord.Embed(
                title="Error Logged",
                description=f"An error occurred in {ctx.guild.name} ({ctx.guild.id})",
                color=discord.Color.red()
            )
            log_embed.add_field(name="User", value=ctx.author.mention, inline=True)
            log_embed.add_field(name="Channel", value=ctx.channel.mention, inline=True)
            log_embed.add_field(name="Command", value=ctx.command, inline=True)
            log_embed.add_field(name="Error", value=str(error), inline=False)
            await log_channel.send(embed=log_embed)

async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))