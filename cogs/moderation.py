import asyncio
import discord
from discord.ext import commands
from discord import app_commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="kick", description="Kicks a member from the server.")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        await member.kick(reason=reason)
        await interaction.response.send_message(f'{member.name} has been kicked. Reason: {reason}')

    @app_commands.command(name="ban", description="Bans a member from the server.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        await member.ban(reason=reason)
        await interaction.response.send_message(f'{member.name} has been banned. Reason: {reason}')

    @app_commands.command(name="unban", description="Unbans a member from the server.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, member: str):
        banned_users = await interaction.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await interaction.guild.unban(user)
                await interaction.response.send_message(f'{user.name}#{user.discriminator} has been unbanned.')
                return

        await interaction.response.send_message(f'{member} was not found.')

    @app_commands.command(name="clear", description="Clears a specified number of messages.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int):
        await interaction.channel.purge(limit=amount + 1)
        await interaction.response.send_message(f'Cleared {amount} messages.', ephemeral=True)

    @app_commands.command(name="mute", description="Mutes a member.")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        muted_role = discord.utils.get(interaction.guild.roles, name="Muted")
        if not muted_role:
            muted_role = await interaction.guild.create_role(name="Muted")
            for channel in interaction.guild.channels:
                await channel.set_permissions(muted_role, speak=False, send_messages=False)
        
        await member.add_roles(muted_role)
        await interaction.response.send_message(f'{member.name} has been muted. Reason: {reason}')

    @app_commands.command(name="unmute", description="Unmutes a member.")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        muted_role = discord.utils.get(interaction.guild.roles, name="Muted")
        await member.remove_roles(muted_role)
        await interaction.response.send_message(f'{member.name} has been unmuted.')

    @app_commands.command(name="timeout", description="Temporarily mutes a member for a specific duration.")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, duration: int, reason: str = None):
        muted_role = discord.utils.get(interaction.guild.roles, name="Muted")
        if not muted_role:
            muted_role = await interaction.guild.create_role(name="Muted")
            for channel in interaction.guild.channels:
                await channel.set_permissions(muted_role, speak=False, send_messages=False)
        
        await member.add_roles(muted_role)
        await interaction.response.send_message(f'{member.name} has been muted for {duration} seconds. Reason: {reason}')
        await asyncio.sleep(duration)
        await member.remove_roles(muted_role)
        await interaction.response.send_message(f'{member.name} has been unmuted after {duration} seconds.')

    @app_commands.command(name="warn", description="Warns a member.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def warn(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        await interaction.response.send_message(f'{member.name} has been warned. Reason: {reason}')

async def setup(bot):
    await bot.add_cog(Moderation(bot))