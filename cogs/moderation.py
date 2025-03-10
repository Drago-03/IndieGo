import discord
from discord.ext import commands
from discord import app_commands
import pandas as pd
import PyPDF2
import os
import asyncio
import logging

logger = logging.getLogger('IndieGOBot')

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

    async def send_response(self, ctx_or_interaction, content, ephemeral=True):
        """Helper method to send responses for both Context and Interaction"""
        if isinstance(ctx_or_interaction, commands.Context):
            await ctx_or_interaction.send(content)
        else:
            if not ctx_or_interaction.response.is_done():
                await ctx_or_interaction.response.send_message(content, ephemeral=ephemeral)
            else:
                await ctx_or_interaction.followup.send(content, ephemeral=ephemeral)

    async def process_massrole_file(self, ctx_or_interaction, attachment, role):
        """Process the uploaded file and assign roles"""
        guild = ctx_or_interaction.guild
        file_name = attachment.filename.lower()
        file_content = await attachment.read()
        user_list = []
        
        try:
            if file_name.endswith(".xlsx"):
                with open("temp.xlsx", "wb") as f:
                    f.write(file_content)
                df = pd.read_excel("temp.xlsx", header=None)
                user_list = df[0].astype(str).tolist()
                os.remove("temp.xlsx")
            
            elif file_name.endswith(".pdf"):
                with open("temp.pdf", "wb") as f:
                    f.write(file_content)
                with open("temp.pdf", "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        user_list.extend(page.extract_text().splitlines())
                os.remove("temp.pdf")
            else:
                await self.send_response(ctx_or_interaction, "Unsupported file format. Please upload an Excel (.xlsx) or PDF file.")
                return
            
            count = 0
            not_found = []
            permission_errors = []
            
            # Send initial response
            await self.send_response(ctx_or_interaction, "Processing role assignments... Please wait.")
            
            for user_info in user_list:
                user_info = user_info.strip()
                if not user_info:
                    continue
                
                try:
                    user = guild.get_member_named(user_info)
                    if user is None and user_info.isdigit():
                        user = guild.get_member(int(user_info))
                    
                    if user is None:
                        not_found.append(user_info)
                        continue
                    
                    await user.add_roles(role)
                    count += 1
                    logger.info(f"Successfully assigned role {role.name} to {user.name}#{user.discriminator}")
                    await asyncio.sleep(0.5)  # Rate limiting to avoid API issues
                    
                except discord.Forbidden:
                    permission_errors.append(user_info)
                    logger.error(f"Permission error while assigning role to {user_info}")
                except discord.HTTPException as e:
                    logger.error(f"HTTP error while assigning role to {user_info}: {str(e)}")
                    await self.send_response(ctx_or_interaction, f"Error assigning role to {user_info}: {str(e)}")
            
            # Send summary
            response = f"✅ Role assigned to {count} users successfully.\n"
            if not_found:
                response += f"\n❌ Users not found ({len(not_found)}):\n" + "\n".join(not_found[:10])
                if len(not_found) > 10:
                    response += f"\n...and {len(not_found) - 10} more"
            if permission_errors:
                response += f"\n⚠️ Permission errors ({len(permission_errors)}):\n" + "\n".join(permission_errors[:10])
                if len(permission_errors) > 10:
                    response += f"\n...and {len(permission_errors) - 10} more"
            
            await self.send_response(ctx_or_interaction, response)
            
            # Log the action
            moderator = ctx_or_interaction.author if isinstance(ctx_or_interaction, commands.Context) else ctx_or_interaction.user
            await self.log_action(guild, f"{moderator.mention} mass-assigned role {role.mention} to {count} users")
            
        except Exception as e:
            logger.error(f"Error in mass role assignment: {str(e)}")
            await self.send_response(ctx_or_interaction, f"An error occurred: {str(e)}")
        finally:
            # Ensure temporary files are cleaned up
            if os.path.exists("temp.xlsx"):
                os.remove("temp.xlsx")
            if os.path.exists("temp.pdf"):
                os.remove("temp.pdf")

    @commands.hybrid_command(
        name="massrole",
        description="Assign a role to multiple users from an Excel or PDF file"
    )
    @commands.has_permissions(manage_roles=True)
    @app_commands.describe(
        role="The role to assign to users"
    )
    async def massrole(self, ctx: commands.Context, role: discord.Role):
        """
        Assign a role to multiple users from an Excel or PDF file
        
        Parameters:
        -----------
        role: The role to assign to the users
        Attachment: An Excel (.xlsx) or PDF file containing usernames or user IDs
        """
        if isinstance(ctx, commands.Context) and not ctx.interaction:
            # Handle prefix command
            if not ctx.message.attachments:
                await ctx.send("Please upload an Excel (.xlsx) or PDF file containing usernames or user IDs.")
                return
            await self.process_massrole_file(ctx, ctx.message.attachments[0], role)
        else:
            # Create a modal for file upload
            modal = discord.ui.Modal(title="Upload File")
            modal.add_item(discord.ui.TextInput(
                label="Please upload the file in your next message",
                style=discord.TextStyle.paragraph,
                required=False,
                default="After clicking submit, send your Excel or PDF file in the next message."
            ))
            
            async def modal_callback(interaction: discord.Interaction):
                await interaction.response.send_message(
                    "Please upload the Excel (.xlsx) or PDF file containing usernames or user IDs.",
                    ephemeral=True
                )
                
                def check(m):
                    return m.author.id == interaction.user.id and m.attachments
                
                try:
                    message = await self.bot.wait_for('message', timeout=60.0, check=check)
                    await self.process_massrole_file(interaction, message.attachments[0], role)
                except asyncio.TimeoutError:
                    await interaction.followup.send("File upload timed out. Please try again.", ephemeral=True)
            
            modal.on_submit = modal_callback
            if isinstance(ctx, commands.Context):
                await ctx.interaction.response.send_modal(modal)
            else:
                await ctx.response.send_modal(modal)

    @app_commands.command(
        name="massrole_upload",
        description="Upload a file to assign roles to multiple users"
    )
    @app_commands.describe(
        role="The role to assign to users",
        file="Excel (.xlsx) or PDF file containing usernames or user IDs"
    )
    async def massrole_upload(
        self,
        interaction: discord.Interaction,
        role: discord.Role,
        file: discord.Attachment
    ):
        """Slash command version of massrole with file upload"""
        if not interaction.user.guild_permissions.manage_roles:
            await interaction.response.send_message("You don't have permission to manage roles!", ephemeral=True)
            return
            
        await interaction.response.defer(ephemeral=True)
        await self.process_massrole_file(interaction, file, role)

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