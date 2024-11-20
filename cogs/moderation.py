import discord
from discord.ext import commands
from discord import app_commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def dm_user(self, user, action, reason, moderator):
        try:
            await user.send(f"You have been {action} by {moderator}.\nReason: {reason}")
        except discord.Forbidden:
            pass

    async def log_action(self, guild, action):
        log_channel = discord.utils.get(guild.text_channels, name="mod-logs")
        if log_channel:
            await log_channel.send(action)

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick_command(self, ctx, member: discord.Member = None, *, reason: str = None):
        if member is None:
            embed = discord.Embed(
                title="Error",
                description="You must specify a member to kick.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        await member.kick(reason=reason)
        await self.dm_user(member, "kicked", reason, ctx.author)
        await self.log_action(ctx.guild, f"{ctx.author} kicked {member}.\nReason: {reason}")
        embed = discord.Embed(
            title="Member Kicked",
            description=f'{member.name} has been kicked. Reason: {reason}',
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

    @app_commands.command(name="kick", description="Kick a member")
    @commands.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member = None, reason: str = None):
        if member is None:
            embed = discord.Embed(
                title="Error",
                description="You must specify a member to kick.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        await member.kick(reason=reason)
        await self.dm_user(member, "kicked", reason, interaction.user)
        await self.log_action(interaction.guild, f"{interaction.user} kicked {member}.\nReason: {reason}")
        embed = discord.Embed(
            title="Member Kicked",
            description=f'{member.name} has been kicked. Reason: {reason}',
            color=discord.Color.orange()
        )
        await interaction.response.send_message(embed=embed)

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban_command(self, ctx, member: discord.Member = None, *, reason: str = None):
        if member is None:
            embed = discord.Embed(
                title="Error",
                description="You must specify a member to ban.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        await member.ban(reason=reason)
        await self.dm_user(member, "banned", reason, ctx.author)
        await self.log_action(ctx.guild, f"{ctx.author} banned {member}.\nReason: {reason}")
        embed = discord.Embed(
            title="Member Banned",
            description=f'{member.name} has been banned. Reason: {reason}',
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

    @app_commands.command(name="ban", description="Ban a member")
    @commands.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member = None, reason: str = None):
        if member is None:
            embed = discord.Embed(
                title="Error",
                description="You must specify a member to ban.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        await member.ban(reason=reason)
        await self.dm_user(member, "banned", reason, interaction.user)
        await self.log_action(interaction.guild, f"{interaction.user} banned {member}.\nReason: {reason}")
        embed = discord.Embed(
            title="Member Banned",
            description=f'{member.name} has been banned. Reason: {reason}',
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)

    @commands.command(name="mute")
    @commands.has_permissions(manage_roles=True)
    async def mute_command(self, ctx, member: discord.Member = None, *, reason: str = None):
        if member is None:
            embed = discord.Embed(
                title="Error",
                description="You must specify a member to mute.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not mute_role:
            mute_role = await ctx.guild.create_role(name="Muted")

            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, speak=False, send_messages=False, read_message_history=True, read_messages=False)

        await member.add_roles(mute_role, reason=reason)
        await self.dm_user(member, "muted", reason, ctx.author)
        await self.log_action(ctx.guild, f"{ctx.author} muted {member}.\nReason: {reason}")
        embed = discord.Embed(
            title="Member Muted",
            description=f'{member.name} has been muted. Reason: {reason}',
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

    @app_commands.command(name="mute", description="Mute a member")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member = None, reason: str = None):
        if member is None:
            embed = discord.Embed(
                title="Error",
                description="You must specify a member to mute.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        mute_role = discord.utils.get(interaction.guild.roles, name="Muted")
        if not mute_role:
            mute_role = await interaction.guild.create_role(name="Muted")

            for channel in interaction.guild.channels:
                await channel.set_permissions(mute_role, speak=False, send_messages=False, read_message_history=True, read_messages=False)

        await member.add_roles(mute_role, reason=reason)
        await self.dm_user(member, "muted", reason, interaction.user)
        await self.log_action(interaction.guild, f"{interaction.user} muted {member}.\nReason: {reason}")
        embed = discord.Embed(
            title="Member Muted",
            description=f'{member.name} has been muted. Reason: {reason}',
            color=discord.Color.orange()
        )
        await interaction.response.send_message(embed=embed)

    @commands.command(name="unmute")
    @commands.has_permissions(manage_roles=True)
    async def unmute_command(self, ctx, member: discord.Member = None, *, reason: str = None):
        if member is None:
            embed = discord.Embed(
                title="Error",
                description="You must specify a member to unmute.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if mute_role in member.roles:
            await member.remove_roles(mute_role)
            await self.dm_user(member, "unmuted", reason, ctx.author)
            await self.log_action(ctx.guild, f"{ctx.author} unmuted {member}.\nReason: {reason}")
            embed = discord.Embed(
                title="Member Unmuted",
                description=f'{member.name} has been unmuted. Reason: {reason}',
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error",
                description=f'{member.name} is not muted.',
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @app_commands.command(name="unmute", description="Unmute a member")
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            embed = discord.Embed(
                title="Error",
                description="You must specify a member to unmute.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        mute_role = discord.utils.get(interaction.guild.roles, name="Muted")
        if mute_role in member.roles:
            await member.remove_roles(mute_role)
            await self.dm_user(member, "unmuted", None, interaction.user)
            await self.log_action(interaction.guild, f"{interaction.user} unmuted {member}.")
            embed = discord.Embed(
                title="Member Unmuted",
                description=f'{member.name} has been unmuted.',
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="Error",
                description=f'{member.name} is not muted.',
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))