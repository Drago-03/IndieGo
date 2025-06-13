import discord
from discord.ext import commands
from discord import app_commands
import pandas as pd
import PyPDF2
import os
import asyncio
import logging
import json
from typing import Optional
from datetime import datetime

logger = logging.getLogger('IndieGOBot')

# Define log colors for different event types
LOG_COLORS = {
    "moderation": discord.Color.red(),           # Moderation actions (kick, ban, etc)
    "role": discord.Color.gold(),                # Role changes
    "member": discord.Color.green(),             # Member joins/leaves
    "message": discord.Color.blue(),             # Message edits/deletes
    "channel": discord.Color.purple(),           # Channel changes
    "server": discord.Color.dark_teal(),         # Server changes
    "bot": discord.Color.dark_magenta(),         # Bot-related actions
    "voice": discord.Color.dark_gold(),          # Voice channel events
    "automod": discord.Color.dark_orange(),      # AutoMod actions
    "setup": discord.Color.teal(),               # Setup actions
    "warning": discord.Color.orange(),           # Warnings
    "success": discord.Color.green(),            # Success messages
    "error": discord.Color.red(),                # Errors
    "info": discord.Color.blue()                 # General info
}

# Define emojis for different log types
LOG_EMOJIS = {
    "moderation": "🛡️",
    "role": "🏷️",
    "member": "👤",
    "message": "💬",
    "channel": "📝",
    "server": "🖥️",
    "bot": "🤖",
    "voice": "🔊",
    "automod": "🔒",
    "setup": "🛠️",
    "warning": "⚠️",
    "success": "✅",
    "error": "❌",
    "info": "ℹ️"
}

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Load configurations from JSON files
        self.autoroles = {}
        self.bot_roles = {}
        self.automod_settings = {}
        self.log_channels = {}  # Store log channel IDs for each guild
        self.load_autoroles()
        self.load_bot_roles()
        self.load_automod_settings()
        self.load_log_channels()

    def load_autoroles(self):
        """Load autoroles from JSON file"""
        try:
            if os.path.exists('autoroles.json'):
                with open('autoroles.json', 'r') as f:
                    self.autoroles = json.load(f)
        except Exception as e:
            logger.error(f"Error loading autoroles: {str(e)}")

    def save_autoroles(self):
        """Save autoroles to JSON file"""
        try:
            with open('autoroles.json', 'w') as f:
                json.dump(self.autoroles, f)
        except Exception as e:
            logger.error(f"Error saving autoroles: {str(e)}")

    def load_bot_roles(self):
        """Load bot roles from JSON file"""
        try:
            if os.path.exists('bot_roles.json'):
                with open('bot_roles.json', 'r') as f:
                    self.bot_roles = json.load(f)
        except Exception as e:
            logger.error(f"Error loading bot roles: {str(e)}")

    def save_bot_roles(self):
        """Save bot roles to JSON file"""
        try:
            with open('bot_roles.json', 'w') as f:
                json.dump(self.bot_roles, f)
        except Exception as e:
            logger.error(f"Error saving bot roles: {str(e)}")

    def load_automod_settings(self):
        """Load automod settings from JSON file"""
        try:
            if os.path.exists('automod_settings.json'):
                with open('automod_settings.json', 'r') as f:
                    self.automod_settings = json.load(f)
        except Exception as e:
            logger.error(f"Error loading automod settings: {str(e)}")
            self.automod_settings = {}

    def save_automod_settings(self):
        """Save automod settings to JSON file"""
        try:
            with open('automod_settings.json', 'w') as f:
                json.dump(self.automod_settings, f)
        except Exception as e:
            logger.error(f"Error saving automod settings: {str(e)}")

    def load_log_channels(self):
        """Load log channel configurations from JSON file"""
        try:
            if os.path.exists('log_channels.json'):
                with open('log_channels.json', 'r') as f:
                    self.log_channels = json.load(f)
        except Exception as e:
            logger.error(f"Error loading log channels: {str(e)}")

    def save_log_channels(self):
        """Save log channel configurations to JSON file"""
        try:
            with open('log_channels.json', 'w') as f:
                json.dump(self.log_channels, f)
        except Exception as e:
            logger.error(f"Error saving log channels: {str(e)}")

    async def create_log_embed(self, title: str, description: str, log_type: str = "info", **kwargs):
        """Create a standardized embed for logging with consistent styling"""
        # Get color and emoji based on log type
        color = kwargs.pop("color", LOG_COLORS.get(log_type, discord.Color.blue()))
        emoji = LOG_EMOJIS.get(log_type, "ℹ️")
        
        # Create embed with timestamp
        embed = discord.Embed(
            title=f"{emoji} {title}",
            description=description,
            color=color,
            timestamp=datetime.utcnow()
        )
        
        # Add any additional fields from kwargs
        for name, value in kwargs.items():
            if value:  # Only add field if value is not empty
                embed.add_field(name=name.replace('_', ' ').title(), value=value, inline=False)
        
        # Add server name in footer for better context
        footer_text = kwargs.pop("footer_text", f"Logged at {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        footer_icon = kwargs.pop("footer_icon", None)
        
        embed.set_footer(text=footer_text, icon_url=footer_icon)
        
        return embed

    async def log_action(self, guild, action, *, log_type="info", title=None, **fields):
        """Enhanced logging function that handles all types of logs with proper styling"""
        try:
            guild_id = str(guild.id)
            if guild_id not in self.log_channels:
                return  # No logging channel configured
                
            channel = guild.get_channel(int(self.log_channels[guild_id]))
            if not channel:
                return  # Channel not found
            
            # Get default title based on log type if not provided
            if title is None:
                title = log_type.title() + " Log"
            
            # Create standardized embed with log type
            embed = await self.create_log_embed(
                title=title,
                description=action,
                log_type=log_type,
                **fields
            )
            
            # Add guild name to footer for context
            embed.set_footer(text=f"{guild.name} • {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
            
            # Send the embed to the logging channel
            await channel.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Error logging action: {str(e)}")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """Log member updates (nickname, roles, etc.)"""
        if before.nick != after.nick:
            await self.log_action(
                after.guild,
                f"Nickname changed for {after.mention}",
                log_type="member",
                title="Nickname Changed",
                before=before.nick or before.name,
                after=after.nick or after.name,
                user_id=after.id
            )
            
        # Role changes
        if before.roles != after.roles:
            added_roles = set(after.roles) - set(before.roles)
            removed_roles = set(before.roles) - set(after.roles)
            
            if added_roles:
                await self.log_action(
                    after.guild,
                    f"Roles added to {after.mention}",
                    log_type="role",
                    title="Roles Added",
                    added_roles=", ".join(role.mention for role in added_roles),
                    user_id=after.id
                )
                
            if removed_roles:
                await self.log_action(
                    after.guild,
                    f"Roles removed from {after.mention}",
                    log_type="role",
                    title="Roles Removed",
                    removed_roles=", ".join(role.mention for role in removed_roles),
                    user_id=after.id
                )

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Log member joins and handle role assignments"""
        # Log the join
        user_created = member.created_at.strftime("%Y-%m-%d %H:%M:%S UTC")
        account_age = (datetime.utcnow() - member.created_at).days
        
        # Set an appropriate thumbnail
        thumbnail = member.display_avatar.url
        
        await self.log_action(
            member.guild,
            f"{member.mention} joined the server",
            log_type="member",
            title="Member Joined",
            member_id=member.id,
            account_created=user_created,
            account_age=f"{account_age} days",
            is_bot="Yes" if member.bot else "No",
            thumbnail=thumbnail
        )
        
        # Handle role assignments (existing code)
        guild_id = str(member.guild.id)
        if member.bot:
            if guild_id in self.bot_roles:
                try:
                    bot_role = member.guild.get_role(int(self.bot_roles[guild_id]))
                    if bot_role:
                        await member.add_roles(bot_role)
                        await self.log_action(
                            member.guild,
                            f"Bot role assigned to {member.mention}",
                            log_type="bot",
                            title="Bot Role Assigned",
                            role=bot_role.mention,
                            thumbnail=member.display_avatar.url
                        )
                        
                        # Remove human autoroles
                        if guild_id in self.autoroles:
                            for role_id in self.autoroles[guild_id]:
                                role = member.guild.get_role(int(role_id))
                                if role and role in member.roles:
                                    await member.remove_roles(role)
                                    await self.log_action(
                                        member.guild,
                                        f"Removed human autorole from bot {member.mention}",
                                        log_type="bot",
                                        title="Autorole Removed",
                                        role=role.mention
                                    )
                except Exception as e:
                    logger.error(f"Error assigning bot role: {str(e)}")
            return
        
        # Handle human autoroles
        if guild_id in self.autoroles:
            for role_id in self.autoroles[guild_id]:
                try:
                    role = member.guild.get_role(int(role_id))
                    if role:
                        await member.add_roles(role)
                        await self.log_action(
                            member.guild,
                            f"Autorole assigned to {member.mention}",
                            log_type="role",
                            title="Autorole Assigned",
                            role=role.mention,
                            thumbnail=member.display_avatar.url
                        )
                except Exception as e:
                    logger.error(f"Error assigning autorole: {str(e)}")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Log member leaves"""
        roles = [role.mention for role in member.roles if role.name != "@everyone"]
        joined_at = member.joined_at.strftime("%Y-%m-%d %H:%M:%S UTC") if member.joined_at else "Unknown"
        
        await self.log_action(
            member.guild,
            f"{member.mention} left the server",
            log_type="member",
            title="Member Left",
            member_id=member.id,
            joined_at=joined_at,
            roles=", ".join(roles) if roles else "No roles",
            is_bot="Yes" if member.bot else "No",
            thumbnail=member.display_avatar.url
        )

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """Log deleted messages"""
        if message.author.bot or not message.guild:
            return
            
        # Create a clean content string, handling attachments
        content = message.content or "No text content"
        if message.attachments:
            content += "\n\nAttachments:\n" + "\n".join(a.url for a in message.attachments)
            
        await self.log_action(
            message.guild,
            f"Message deleted in {message.channel.mention}",
            log_type="message",
            title="Message Deleted",
            author=f"{message.author.mention} ({message.author.id})",
            content=content[:1024],  # Discord embed field value limit
            channel=message.channel.mention,
            thumbnail=message.author.display_avatar.url
        )

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """Log edited messages"""
        if before.author.bot or before.content == after.content or not before.guild:
            return
            
        await self.log_action(
            after.guild,
            f"Message edited in {after.channel.mention}",
            log_type="message",
            title="Message Edited",
            author=f"{after.author.mention} ({after.author.id})",
            before=before.content[:1024],
            after=after.content[:1024],
            jump_url=f"[Go to message]({after.jump_url})",
            thumbnail=after.author.display_avatar.url
        )

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        """Log role creation"""
        await self.log_action(
            role.guild,
            f"Role created: {role.mention}",
            log_type="role",
            title="Role Created",
            role_id=role.id,
            permissions=", ".join(perm for perm, value in role.permissions if value),
            color=str(role.color),
            position=role.position
        )

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        """Log role deletion"""
        await self.log_action(
            role.guild,
            f"Role deleted: {role.name}",
            log_type="role",
            title="Role Deleted",
            role_id=role.id,
            role_name=role.name,
            color=str(role.color),
            position=role.position
        )

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        """Log role updates"""
        if before.name != after.name:
            await self.log_action(
                after.guild,
                f"Role renamed: {after.mention}",
                log_type="role",
                title="Role Renamed",
                before_name=before.name,
                after_name=after.name
            )
            
        if before.permissions != after.permissions:
            # Find changed permissions
            changes = []
            for perm, value in after.permissions:
                if getattr(before.permissions, perm) != value:
                    changes.append(f"{perm}: {getattr(before.permissions, perm)} → {value}")
                    
            await self.log_action(
                after.guild,
                f"Role permissions updated: {after.mention}",
                log_type="role",
                title="Role Permissions Updated",
                changes="\n".join(changes)
            )
            
        if before.color != after.color:
            await self.log_action(
                after.guild,
                f"Role color updated: {after.mention}",
                log_type="role",
                title="Role Color Updated",
                before_color=str(before.color),
                after_color=str(after.color)
            )

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        """Log channel creation"""
        await self.log_action(
            channel.guild,
            f"Channel created: {channel.mention}",
            log_type="channel",
            title="Channel Created",
            channel_id=channel.id,
            channel_type=str(channel.type),
            category=channel.category.name if channel.category else "None"
        )

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        """Log channel deletion"""
        await self.log_action(
            channel.guild,
            f"Channel deleted: #{channel.name}",
            log_type="channel",
            title="Channel Deleted",
            channel_id=channel.id,
            channel_type=str(channel.type),
            category=channel.category.name if channel.category else "None"
        )

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        """Log channel updates"""
        if before.name != after.name:
            await self.log_action(
                after.guild,
                f"Channel renamed: {after.mention}",
                log_type="channel",
                title="Channel Renamed",
                before_name=before.name,
                after_name=after.name
            )
            
        if before.category != after.category:
            await self.log_action(
                after.guild,
                f"Channel moved: {after.mention}",
                log_type="channel",
                title="Channel Moved",
                before_category=before.category.name if before.category else "None",
                after_category=after.category.name if after.category else "None"
            )

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Log voice channel events"""
        if not before.channel and after.channel:
            await self.log_action(
                member.guild,
                f"{member.mention} joined voice channel {after.channel.mention}",
                log_type="voice",
                title="Voice Channel Joined",
                member_id=member.id,
                channel=after.channel.mention
            )
        elif before.channel and not after.channel:
            await self.log_action(
                member.guild,
                f"{member.mention} left voice channel {before.channel.mention}",
                log_type="voice",
                title="Voice Channel Left",
                member_id=member.id,
                channel=before.channel.mention
            )
        elif before.channel and after.channel and before.channel != after.channel:
            await self.log_action(
                member.guild,
                f"{member.mention} moved from {before.channel.mention} to {after.channel.mention}",
                log_type="voice",
                title="Voice Channel Moved",
                member_id=member.id,
                before_channel=before.channel.mention,
                after_channel=after.channel.mention
            )

    @commands.hybrid_command(
        name="setup",
        description="Setup all moderation features including roles, logs, and automod"
    )
    @commands.has_permissions(administrator=True)
    async def setup_command(self, ctx):
        """Setup all moderation features including roles, logs, and automod"""
        if not ctx.guild:
            await ctx.send("This command can only be used in a server!")
            return

        # Create initial embed
        embed = discord.Embed(
            title="🛠️ Server Setup Progress",
            description="Setting up moderation features...",
            color=discord.Color.blue()
        )
        
        # Handle both prefix and slash commands
        if isinstance(ctx, commands.Context):
            setup_msg = await ctx.send(embed=embed)
        else:
            await ctx.response.send_message(embed=embed)
            setup_msg = await ctx.original_response()

        # Function to update progress
        async def update_progress(status, success=True):
            embed = setup_msg.embeds[0]
            emoji = "✅" if success else "❌"
            embed.add_field(name=f"{emoji} {status}", value="", inline=False)
            await setup_msg.edit(embed=embed)

        try:
            # 1. Setup Logging Channel
            embed.add_field(name="📝 Setting up Logging Channel...", value="", inline=False)
            await setup_msg.edit(embed=embed)
            
            # Create logs category if it doesn't exist
            logs_category = discord.utils.get(ctx.guild.categories, name="Server Logs")
            if not logs_category:
                try:
                    logs_category = await ctx.guild.create_category(
                        "Server Logs",
                        position=0,  # Place at top
                        reason="Automatic logs category creation"
                    )
                    # Set category permissions
                    await logs_category.set_permissions(ctx.guild.default_role, read_messages=False)
                    await logs_category.set_permissions(ctx.guild.me, read_messages=True, send_messages=True)
                except discord.Forbidden:
                    await update_progress("Failed to create logs category - Missing permissions", False)
                    return
            
            # Create or get the logging channel
            log_channel = discord.utils.get(ctx.guild.text_channels, name="mod-logs")
            if not log_channel:
                try:
                    log_channel = await ctx.guild.create_text_channel(
                        "mod-logs",
                        category=logs_category,
                        topic="Server logs - All moderation actions, member updates, and server changes",
                        reason="Automatic logging channel creation",
                        slowmode_delay=5  # Prevent spam
                    )
                    
                    # Set specific permissions
                    await log_channel.set_permissions(ctx.guild.default_role, read_messages=False)
                    await log_channel.set_permissions(ctx.guild.me, read_messages=True, send_messages=True)
                    
                    # Store the log channel ID
                    self.log_channels[str(ctx.guild.id)] = str(log_channel.id)
                    self.save_log_channels()
                    
                    await update_progress("Created logging channel")
                except discord.Forbidden:
                    await update_progress("Failed to create logging channel - Missing permissions", False)
                    return
            else:
                self.log_channels[str(ctx.guild.id)] = str(log_channel.id)
                self.save_log_channels()
                await update_progress("Logging channel found and configured")

            # 2. Setup Bot Role and Management
            embed.add_field(name="🤖 Checking Bot Role Management...", value="", inline=False)
            await setup_msg.edit(embed=embed)
            
            bot_role_setup = await self.setup_bot_roles(ctx.guild)
            if bot_role_setup:
                await update_progress("Bot role management configured")
            else:
                await update_progress("No bot role found - Skipping bot role management")

            # 3. Setup Quarantine Role
            embed.add_field(name="🔍 Checking Quarantine Role...", value="", inline=False)
            await setup_msg.edit(embed=embed)
            
            quarantine_role = discord.utils.get(ctx.guild.roles, name="Quarantine")
            if not quarantine_role:
                try:
                    quarantine_role = await ctx.guild.create_role(
                        name="Quarantine",
                        color=discord.Color.red(),
                        reason="Automatic quarantine role creation"
                    )
                    await update_progress("Created Quarantine role")
                except discord.Forbidden:
                    await update_progress("Failed to create Quarantine role - Missing permissions", False)
                    return
            else:
                await update_progress("Quarantine role found")

            # 4. Setup Muted Role
            embed.add_field(name="🔍 Checking Muted Role...", value="", inline=False)
            await setup_msg.edit(embed=embed)
            
            muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
            if not muted_role:
                try:
                    muted_role = await ctx.guild.create_role(
                        name="Muted",
                        color=discord.Color.dark_grey(),
                        reason="Automatic muted role creation"
                    )
                    await update_progress("Created Muted role")
                except discord.Forbidden:
                    await update_progress("Failed to create Muted role - Missing permissions", False)
                    return
            else:
                await update_progress("Muted role found")

            # 5. Configure Muted Role Permissions
            embed.add_field(name="⚙️ Configuring Muted Role Permissions...", value="", inline=False)
            await setup_msg.edit(embed=embed)
            
            try:
                for channel in ctx.guild.channels:
                    if isinstance(channel, (discord.TextChannel, discord.VoiceChannel)):
                        await channel.set_permissions(
                            muted_role,
                            send_messages=False,
                            add_reactions=False,
                            speak=False,
                            stream=False,
                            create_public_threads=False,
                            create_private_threads=False,
                            send_messages_in_threads=False
                        )
                await update_progress("Configured Muted role permissions")
            except discord.Forbidden:
                await update_progress("Failed to configure Muted role permissions - Missing permissions", False)
                return

            # 6. Verify and Update Autoroles
            embed.add_field(name="👥 Verifying Autorole Assignments...", value="", inline=False)
            await setup_msg.edit(embed=embed)
            
            if str(ctx.guild.id) in self.autoroles:
                try:
                    # Check and update role assignments
                    human_count = 0
                    bot_count = 0
                    for member in ctx.guild.members:
                        if member.bot:
                            # Remove human autoroles from bots
                            for role_id in self.autoroles[str(ctx.guild.id)]:
                                role = ctx.guild.get_role(int(role_id))
                                if role and role in member.roles:
                                    await member.remove_roles(role)
                                    bot_count += 1
                            
                            # Add bot role if it exists
                            if str(ctx.guild.id) in self.bot_roles:
                                bot_role = ctx.guild.get_role(int(self.bot_roles[str(ctx.guild.id)]))
                                if bot_role and bot_role not in member.roles:
                                    await member.add_roles(bot_role)
                        else:
                            # Ensure humans have their autoroles
                            for role_id in self.autoroles[str(ctx.guild.id)]:
                                role = ctx.guild.get_role(int(role_id))
                                if role and role not in member.roles:
                                    await member.add_roles(role)
                                    human_count += 1
                    
                    await update_progress(f"Updated autoroles (Humans: {human_count}, Bots: {bot_count})")
                except Exception as e:
                    await update_progress(f"Error updating autoroles: {str(e)}", False)
            else:
                await update_progress("No autoroles configured - Skipping verification")

            # 7. Setup AutoMod
            embed.add_field(name="🛡️ Setting up AutoMod...", value="", inline=False)
            await setup_msg.edit(embed=embed)
            
            try:
                # Initialize automod settings if not exists
                if str(ctx.guild.id) not in self.automod_settings:
                    self.automod_settings[str(ctx.guild.id)] = {
                        "enabled": True,
                        "word_filter": [],
                        "spam_threshold": 5,
                        "mention_threshold": 5,
                        "caps_threshold": 70,
                        "link_filter": True,
                        "invite_filter": True,
                        "punishment": "mute",
                        "punishment_duration": 3600  # 1 hour in seconds
                    }
                    self.save_automod_settings()
                    await update_progress("Initialized AutoMod settings")
                else:
                    await update_progress("AutoMod settings found")

            except Exception as e:
                await update_progress(f"Failed to setup AutoMod: {str(e)}", False)
                return

            # Final success message
            embed.color = discord.Color.green()
            embed.description = "✅ Server setup completed successfully!"
            await setup_msg.edit(embed=embed)
            
            # Log the setup completion
            await self.log_action(
                ctx.guild,
                f"Server setup completed by {ctx.author.mention}",
                log_type="setup",
                title="Server Setup Complete",
                setup_by=ctx.author.mention,
                logging_channel=log_channel.mention
            )

        except Exception as e:
            embed.color = discord.Color.red()
            embed.description = f"❌ Setup failed: {str(e)}"
            await setup_msg.edit(embed=embed)
            logger.error(f"Setup failed: {str(e)}")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """Handle bot role setup when joining a new server"""
        await self.setup_bot_roles(guild)

    async def setup_bot_roles(self, guild):
        """Setup bot roles for a server"""
        try:
            # Check for existing bot role
            bot_role = discord.utils.get(guild.roles, name="Bot")
            
            # If bot role exists, store it
            if bot_role:
                self.bot_roles[str(guild.id)] = str(bot_role.id)
                self.save_bot_roles()
                logger.info(f"Found existing bot role in {guild.name}")
                
                # Assign role to all bots and remove human autoroles
                bot_count = 0
                for member in guild.members:
                    if member.bot:
                        try:
                            # Remove any human autoroles from bots
                            if str(guild.id) in self.autoroles:
                                for role_id in self.autoroles[str(guild.id)]:
                                    role = guild.get_role(int(role_id))
                                    if role and role in member.roles:
                                        await member.remove_roles(role)
                                        logger.info(f"Removed human autorole from bot {member.name} in {guild.name}")
                            
                            # Add bot role if not already assigned
                            if bot_role not in member.roles:
                                await member.add_roles(bot_role)
                                bot_count += 1
                        except discord.Forbidden:
                            logger.error(f"Missing permissions to manage roles for {member.name} in {guild.name}")
                        except Exception as e:
                            logger.error(f"Error managing roles for {member.name} in {guild.name}: {str(e)}")
                
                logger.info(f"Updated roles for {bot_count} bots in {guild.name}")
                return True
            
            return False  # No bot role exists
            
        except Exception as e:
            logger.error(f"Error in setup_bot_roles for {guild.name}: {str(e)}")
            return False

    @commands.hybrid_command(
        name="autorole_add",
        description="Add a role to be automatically assigned to new members"
    )
    @commands.has_permissions(manage_roles=True)
    @app_commands.describe(role="The role to automatically assign to new members")
    async def autorole_add(self, ctx, role: discord.Role):
        """Add a role to be automatically assigned to new members"""
        guild_id = str(ctx.guild.id)
        
        # Initialize if guild not in autoroles
        if guild_id not in self.autoroles:
            self.autoroles[guild_id] = []
            
        # Check if role is already in autoroles
        if str(role.id) in self.autoroles[guild_id]:
            await ctx.send(f"❌ {role.mention} is already set as an autorole!", ephemeral=True)
            return
            
        # Add role to autoroles
        self.autoroles[guild_id].append(str(role.id))
        self.save_autoroles()
        
        await ctx.send(f"✅ Added {role.mention} to autoroles! New members will automatically receive this role.", ephemeral=True)
        await self.log_action(ctx.guild, f"{ctx.author.mention} added {role.mention} to autoroles")

    @commands.hybrid_command(
        name="autorole_remove",
        description="Remove a role from being automatically assigned"
    )
    @commands.has_permissions(manage_roles=True)
    @app_commands.describe(role="The role to remove from auto-assignment")
    async def autorole_remove(self, ctx, role: discord.Role):
        """Remove a role from being automatically assigned"""
        guild_id = str(ctx.guild.id)
        
        if guild_id not in self.autoroles or str(role.id) not in self.autoroles[guild_id]:
            await ctx.send(f"❌ {role.mention} is not set as an autorole!", ephemeral=True)
            return
            
        self.autoroles[guild_id].remove(str(role.id))
        self.save_autoroles()
        
        await ctx.send(f"✅ Removed {role.mention} from autoroles!", ephemeral=True)
        await self.log_action(ctx.guild, f"{ctx.author.mention} removed {role.mention} from autoroles")

    @commands.hybrid_command(
        name="autorole_list",
        description="List all roles that are automatically assigned"
    )
    @commands.has_permissions(manage_roles=True)
    async def autorole_list(self, ctx):
        """List all roles that are automatically assigned"""
        guild_id = str(ctx.guild.id)
        
        if guild_id not in self.autoroles or not self.autoroles[guild_id]:
            await ctx.send("❌ No autoroles are set up for this server!", ephemeral=True)
            return
            
        embed = discord.Embed(
            title="Autoroles",
            description="The following roles are automatically assigned to new members:",
            color=discord.Color.blue()
        )
        
        for role_id in self.autoroles[guild_id]:
            role = ctx.guild.get_role(int(role_id))
            if role:
                embed.add_field(name=role.name, value=f"ID: {role.id}", inline=False)
            
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(
        name="autorole_clear",
        description="Clear all autoroles for this server"
    )
    @commands.has_permissions(manage_roles=True)
    async def autorole_clear(self, ctx):
        """Clear all autoroles for this server"""
        guild_id = str(ctx.guild.id)
        
        if guild_id not in self.autoroles or not self.autoroles[guild_id]:
            await ctx.send("❌ No autoroles are set up for this server!", ephemeral=True)
            return
            
        self.autoroles[guild_id] = []
        self.save_autoroles()
        
        await ctx.send("✅ Cleared all autoroles for this server!", ephemeral=True)
        await self.log_action(ctx.guild, f"{ctx.author.mention} cleared all autoroles")

    async def dm_user(self, user, action, reason, moderator):
        try:
            await user.send(f"You have been {action} by {moderator}.\nReason: {reason}")
        except discord.Forbidden:
            pass

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
            already_have_role = []
            bots_skipped = []
            
            # Send initial response
            await self.send_response(ctx_or_interaction, "Processing role assignments... Please wait.")
            
            total = len(user_list)
            progress_msg = await ctx_or_interaction.channel.send(f"Progress: 0/{total} users processed")

            # Process users in batches
            batch_size = 10  # Process 10 users at a time
            for i in range(0, len(user_list), batch_size):
                batch = user_list[i:i + batch_size]
                tasks = []
                
                for user_info in batch:
                    user_info = user_info.strip()
                    if not user_info:
                        continue
                    
                    user = guild.get_member_named(user_info)
                    if user is None and user_info.isdigit():
                        user = guild.get_member(int(user_info))
                    
                    if user is None:
                        not_found.append(user_info)
                        continue
                    
                    # Skip bots and log them
                    if user.bot:
                        bots_skipped.append(user_info)
                        # Ensure bot has the bot role if it exists
                        if str(guild.id) in self.bot_roles:
                            bot_role = guild.get_role(int(self.bot_roles[str(guild.id)]))
                            if bot_role and bot_role not in user.roles:
                                try:
                                    await user.add_roles(bot_role)
                                except discord.Forbidden:
                                    logger.error(f"Failed to assign bot role to {user.name}")
                        continue
                    
                    if role in user.roles:
                        already_have_role.append(user_info)
                        continue
                    
                    # Add role assignment task to batch
                    tasks.append(user.add_roles(role))
                
                if tasks:
                    # Execute batch of role assignments concurrently
                    try:
                        await asyncio.gather(*tasks)
                        count += len(tasks)
                    except discord.Forbidden as e:
                        permission_errors.extend([user_info for user_info in batch])
                        logger.error(f"Permission error while assigning roles: {str(e)}")
                    except discord.HTTPException as e:
                        logger.error(f"HTTP error while assigning roles: {str(e)}")
                
                # Update progress every batch
                processed = count + len(not_found) + len(already_have_role) + len(bots_skipped)
                await progress_msg.edit(content=f"Progress: {processed}/{total} users processed")
                
                # Small delay between batches to prevent rate limiting
                await asyncio.sleep(0.5)
            
            # Send summary
            embed = discord.Embed(
                title=f"Mass Role Assignment Complete - {role.name}",
                description=f"Role assignment results for {role.mention}:",
                color=role.color if role.color != discord.Color.default() else discord.Color.blue()
            )
            embed.add_field(name="Success", value=f"✅ Role assigned to {count} users", inline=False)
            if already_have_role:
                embed.add_field(name="Skipped", value=f"⏭️ {len(already_have_role)} users already had {role.mention}", inline=False)
            if bots_skipped:
                embed.add_field(name="Bots Skipped", value=f"🤖 {len(bots_skipped)} bots were skipped and assigned bot role", inline=False)
            if not_found:
                embed.add_field(name="Not Found", value=f"❓ {len(not_found)} users not found", inline=False)
            if permission_errors:
                embed.add_field(name="Failed", value=f"❌ Failed to assign role to {len(permission_errors)} users", inline=False)
            
            # Add role information
            embed.add_field(
                name="Role Details",
                value=(
                    f"• Name: {role.name}\n"
                    f"• ID: {role.id}\n"
                    f"• Color: {str(role.color)}\n"
                    f"• Position: {role.position}\n"
                    f"• Mentionable: {'Yes' if role.mentionable else 'No'}"
                ),
                inline=False
            )
            
            # Set role color as embed color if available
            if role.icon:
                embed.set_thumbnail(url=role.icon.url)
            
            await progress_msg.edit(content=None, embed=embed)
            
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

    @app_commands.command(
        name="massrole",
        description="Assign a role to all server members or specific users from a file"
    )
    @app_commands.describe(
        role="The role to assign to users"
    )
    @commands.has_permissions(manage_roles=True)
    async def massrole_slash(
        self, 
        interaction: discord.Interaction, 
        role: discord.Role
    ):
        """Slash command version of massrole"""
        ctx = await self.bot.get_context(interaction)
        await self.massrole(ctx, role)

    @commands.command(
        name="massrole",
        description="Assign a role to all server members or specific users from a file"
    )
    @commands.has_permissions(manage_roles=True)
    async def massrole(
        self, 
        ctx, 
        role: discord.Role
    ):
        """
        Assign a role to all server members or specific users from a file
        
        Parameters:
        -----------
        role: The role to assign to the users
        
        Usage:
        ------
        • Without file: Assigns role to all human members (bots are skipped)
        • With file: Attach an Excel (.xlsx) or PDF file containing usernames/IDs
        """
        if not ctx.guild:
            await ctx.send("This command can only be used in a server!")
            return

        # Check for file attachment
        file = None
        if isinstance(ctx, commands.Context) and ctx.message.attachments:
            file = ctx.message.attachments[0]
        elif isinstance(ctx, discord.Interaction) and ctx.data.get('attachments'):
            file = ctx.data['attachments'][0]

        if file:
            # Handle file-based role assignment
            await self.process_massrole_file(ctx, file, role)
            return

        # Handle mass role assignment to all human members
        await ctx.send(f"🔄 Starting mass role assignment of {role.mention} to all human members...")
        
        count = 0
        failed = 0
        skipped = 0
        bots_skipped = 0
        
        # Get all human members
        members = [m for m in ctx.guild.members if not m.bot]
        total = len(members)
        
        # Create progress message
        progress_msg = await ctx.send(f"Progress: 0/{total} members processed")
        
        # Process members in batches
        batch_size = 10  # Process 10 members at a time
        for i in range(0, len(members), batch_size):
            batch = members[i:i + batch_size]
            tasks = []
            
            for member in batch:
                if role in member.roles:
                    skipped += 1
                    continue
                
                tasks.append(member.add_roles(role))
            
            if tasks:
                try:
                    # Execute batch of role assignments concurrently
                    await asyncio.gather(*tasks)
                    count += len(tasks)
                except discord.Forbidden:
                    failed += len(tasks)
                    logger.error(f"Permission error while assigning roles to batch")
                except discord.HTTPException as e:
                    failed += len(tasks)
                    logger.error(f"HTTP error while assigning roles to batch: {str(e)}")
            
            # Update progress every batch
            processed = count + skipped + failed
            await progress_msg.edit(content=f"Progress: {processed}/{total} members processed")
            
            # Small delay between batches to prevent rate limiting
            await asyncio.sleep(0.5)
        
        # Send final summary
        embed = discord.Embed(
            title=f"Mass Role Assignment Complete - {role.name}",
            description=f"Role assignment results for {role.mention}:",
            color=role.color if role.color != discord.Color.default() else discord.Color.blue()
        )
        embed.add_field(name="Success", value=f"✅ Role assigned to {count} members", inline=False)
        embed.add_field(name="Skipped", value=f"⏭️ {skipped} members already had {role.mention}", inline=False)
        embed.add_field(name="Bots Skipped", value=f"🤖 {len([m for m in ctx.guild.members if m.bot])} bots were skipped", inline=False)
        if failed > 0:
            embed.add_field(name="Failed", value=f"❌ Failed to assign role to {failed} members", inline=False)

        # Add role information
        embed.add_field(
            name="Role Details",
            value=(
                f"• Name: {role.name}\n"
                f"• ID: {role.id}\n"
                f"• Color: {str(role.color)}\n"
                f"• Position: {role.position}\n"
                f"• Mentionable: {'Yes' if role.mentionable else 'No'}"
            ),
            inline=False
        )

        # Set role color as embed color if available
        if role.icon:
            embed.set_thumbnail(url=role.icon.url)
        
        await progress_msg.edit(content=None, embed=embed)
        await self.log_action(ctx.guild, f"{ctx.author.mention} mass-assigned role {role.mention} to {count} members")

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

    @commands.hybrid_command(
        name="botrole_add",
        description="Set a role to be automatically assigned to bots"
    )
    @commands.has_permissions(manage_roles=True)
    @app_commands.describe(role="The role to automatically assign to bots")
    async def botrole_add(self, ctx, role: discord.Role):
        """Set a role to be automatically assigned to bots"""
        guild_id = str(ctx.guild.id)
        
        # Check if role is already set as bot role
        if guild_id in self.bot_roles and str(role.id) == self.bot_roles[guild_id]:
            await ctx.send(f"❌ {role.mention} is already set as the bot role!", ephemeral=True)
            return
            
        # Store the new bot role
        self.bot_roles[guild_id] = str(role.id)
        self.save_bot_roles()
        
        # Create embed for response
        embed = discord.Embed(
            title="🤖 Bot Role Added",
            description=f"{role.mention} will now be automatically assigned to all bots.",
            color=role.color if role.color != discord.Color.default() else discord.Color.blue()
        )
        
        # Add role details
        embed.add_field(
            name="Role Details",
            value=(
                f"• Name: {role.name}\n"
                f"• ID: {role.id}\n"
                f"• Color: {str(role.color)}\n"
                f"• Position: {role.position}\n"
                f"• Mentionable: {'Yes' if role.mentionable else 'No'}"
            ),
            inline=False
        )
        
        # Add current bot count
        bot_count = len([m for m in ctx.guild.members if m.bot])
        embed.add_field(
            name="Current Bots",
            value=f"There are currently {bot_count} bots in the server.",
            inline=False
        )
        
        # Ask if user wants to assign role to existing bots
        embed.add_field(
            name="Existing Bots",
            value="Would you like to assign this role to all existing bots? React with ✅ to confirm.",
            inline=False
        )
        
        # Send response
        message = await ctx.send(embed=embed)
        await message.add_reaction("✅")
        
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == "✅" and reaction.message.id == message.id
        
        try:
            # Wait for reaction
            await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
            
            # User confirmed, assign roles to existing bots
            progress_msg = await ctx.send(f"🔄 Assigning {role.mention} to existing bots...")
            assigned = 0
            failed = 0
            
            for member in ctx.guild.members:
                if member.bot:
                    try:
                        if role not in member.roles:
                            await member.add_roles(role)
                            assigned += 1
                            # Remove any human autoroles
                            if guild_id in self.autoroles:
                                for autorole_id in self.autoroles[guild_id]:
                                    autorole = ctx.guild.get_role(int(autorole_id))
                                    if autorole and autorole in member.roles:
                                        await member.remove_roles(autorole)
                    except discord.Forbidden:
                        failed += 1
                        logger.error(f"Failed to assign bot role to {member.name}")
                    except Exception as e:
                        failed += 1
                        logger.error(f"Error assigning bot role to {member.name}: {str(e)}")
                    
                    # Add small delay to prevent rate limiting
                    await asyncio.sleep(0.5)
            
            # Update progress message with results
            await progress_msg.edit(content=f"✅ Assigned {role.mention} to {assigned} bots" + (f"\n❌ Failed to assign to {failed} bots" if failed > 0 else ""))
            
        except asyncio.TimeoutError:
            await message.edit(content="Role has been set as bot role, but no roles were assigned to existing bots.")
        
        await self.log_action(ctx.guild, f"{ctx.author.mention} set {role.mention} as the bot role")

    @commands.hybrid_command(
        name="botrole_remove",
        description="Remove the automatic bot role assignment"
    )
    @commands.has_permissions(manage_roles=True)
    async def botrole_remove(self, ctx):
        """Remove the automatic bot role assignment"""
        guild_id = str(ctx.guild.id)
        
        if guild_id not in self.bot_roles:
            await ctx.send("❌ No bot role is currently set!", ephemeral=True)
            return
        
        # Get the current bot role before removing it
        role = ctx.guild.get_role(int(self.bot_roles[guild_id]))
        role_mention = role.mention if role else "Unknown Role"
        
        # Remove the bot role configuration
        del self.bot_roles[guild_id]
        self.save_bot_roles()
        
        embed = discord.Embed(
            title="🤖 Bot Role Removed",
            description=f"Removed {role_mention} from automatic bot role assignment.",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="Note",
            value="Existing bots will keep their roles, but new bots won't receive the role automatically.",
            inline=False
        )
        
        await ctx.send(embed=embed)
        await self.log_action(ctx.guild, f"{ctx.author.mention} removed {role_mention} as the bot role")

    @commands.hybrid_command(
        name="botrole_list",
        description="Show the current bot role configuration"
    )
    @commands.has_permissions(manage_roles=True)
    async def botrole_list(self, ctx):
        """Show the current bot role configuration"""
        guild_id = str(ctx.guild.id)
        
        if guild_id not in self.bot_roles:
            await ctx.send("❌ No bot role is currently set!", ephemeral=True)
            return
        
        role = ctx.guild.get_role(int(self.bot_roles[guild_id]))
        if not role:
            await ctx.send("❌ The configured bot role no longer exists!", ephemeral=True)
            return
        
        # Create embed with role information
        embed = discord.Embed(
            title="🤖 Bot Role Configuration",
            description=f"Current bot role: {role.mention}",
            color=role.color if role.color != discord.Color.default() else discord.Color.blue()
        )
        
        # Add role details
        embed.add_field(
            name="Role Details",
            value=(
                f"• Name: {role.name}\n"
                f"• ID: {role.id}\n"
                f"• Color: {str(role.color)}\n"
                f"• Position: {role.position}\n"
                f"• Mentionable: {'Yes' if role.mentionable else 'No'}"
            ),
            inline=False
        )
        
        # Add bot statistics
        bots_with_role = len([m for m in ctx.guild.members if m.bot and role in m.roles])
        total_bots = len([m for m in ctx.guild.members if m.bot])
        
        embed.add_field(
            name="Statistics",
            value=(
                f"• Total Bots: {total_bots}\n"
                f"• Bots with Role: {bots_with_role}\n"
                f"• Bots without Role: {total_bots - bots_with_role}"
            ),
            inline=False
        )
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Moderation(bot))