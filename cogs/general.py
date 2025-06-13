import random
import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
from config import SUPPORT_SERVER_LINK, BOT_WEBSITE, AUTHOR_NAME, AUTHOR_ICON, EMBED_COLOR, COPYRIGHT, ATTRIBUTION
import platform
import time
import psutil
import datetime
import os
import logging

logger = logging.getLogger('IndieGOBot')

# Define test guild IDs for faster command registration during development
TEST_GUILD_IDS = [1308525132620914688, 1223008803138699315]  # Match the ID from main.py

class ProfileView(View):
    def __init__(self, member):
        super().__init__(timeout=60)
        self.member = member

    @discord.ui.button(label="User Avatar", style=discord.ButtonStyle.primary)
    async def user_avatar(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="User Avatar", color=discord.Color.blue())
        embed.set_image(url=self.member.avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Server Avatar", style=discord.ButtonStyle.primary)
    async def server_avatar(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Server Avatar", color=discord.Color.blue())
        embed.set_image(url=self.member.display_avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="User Banner", style=discord.ButtonStyle.primary)
    async def user_banner(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.member.banner:
            embed = discord.Embed(title="User Banner", color=discord.Color.blue())
            embed.set_image(url=self.member.banner.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message("You do not have a banner set.", ephemeral=True)

    @discord.ui.button(label="Server Banner", style=discord.ButtonStyle.primary)
    async def server_banner(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.guild.banner:
            embed = discord.Embed(title="Server Banner", color=discord.Color.blue())
            embed.set_image(url=interaction.guild.banner.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message("This server does not have a banner set.", ephemeral=True)

class AboutView(View):
    def __init__(self, bot):
        super().__init__(timeout=120)
        self.bot = bot
        
    @discord.ui.button(label="Support Server", style=discord.ButtonStyle.primary, emoji="🛠️")
    async def support_server(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"Join our support server: {SUPPORT_SERVER_LINK}", ephemeral=True)
        
    @discord.ui.button(label="Invite Bot", style=discord.ButtonStyle.success, emoji="✉️")
    async def invite_bot(self, interaction: discord.Interaction, button: discord.ui.Button):
        invite_link = f"https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot%20applications.commands"
        await interaction.response.send_message(f"Invite IndieGO to your server: {invite_link}", ephemeral=True)
        
    @discord.ui.button(label="Website", style=discord.ButtonStyle.link, url=BOT_WEBSITE, emoji="🌐")
    async def website(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass
        
    @discord.ui.button(label="Owner Profile", style=discord.ButtonStyle.secondary, emoji="👑")
    async def owner_profile(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            owner = await self.bot.fetch_user(950609706760691752)  # Owner ID
            embed = discord.Embed(
                title=f"👑 Bot Owner",
                description=f"**{owner.name}**",
                color=EMBED_COLOR
            )
            embed.set_thumbnail(url=owner.display_avatar.url)
            embed.add_field(name="ID", value=f"`{owner.id}`", inline=True)
            embed.add_field(name="Created At", value=f"<t:{int(owner.created_at.timestamp())}:R>", inline=True)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Could not fetch owner information: {str(e)}", ephemeral=True)

class General(commands.Cog):
    """General bot commands"""
    
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.datetime.utcnow()
        logger.info("General cog initialized")

    def get_bot_uptime(self):
        """Get the bot's uptime in a human-readable format"""
        current_time = datetime.datetime.utcnow()
        delta = current_time - self.start_time
        
        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if days > 0:
            return f"{days}d {hours}h {minutes}m {seconds}s"
        elif hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"

    def get_system_info(self):
        """Get system information"""
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_used = round(memory.used / (1024 * 1024 * 1024), 2)  # GB
        memory_total = round(memory.total / (1024 * 1024 * 1024), 2)  # GB
        
        return {
            "cpu": cpu_percent,
            "memory_used": memory_used,
            "memory_total": memory_total,
            "memory_percent": memory_percent
        }

    # SUPER BASIC PREFIX COMMAND VERSION
    @commands.command(name="ping")
    async def ping_command(self, ctx):
        """Check bot latency using prefix command"""
        try:
            # Just send a simple message first to confirm the command works
            await ctx.send(f"🏓 Pong! Bot latency: {round(self.bot.latency * 1000)}ms")
        except Exception as e:
            logger.error(f"Error in ping command: {str(e)}")
            await ctx.send(f"Error: {str(e)}")

    # SUPER BASIC SLASH COMMAND VERSION
    @app_commands.command(name="ping", description="Check the bot's latency")
    async def ping_slash(self, interaction: discord.Interaction):
        """Check bot latency using slash command"""
        try:
            await interaction.response.send_message(f"🏓 Pong! Bot latency: {round(self.bot.latency * 1000)}ms")
        except Exception as e:
            logger.error(f"Error in ping slash command: {str(e)}")
            await interaction.response.send_message(f"Error: {str(e)}")

    # SUPER BASIC PREFIX COMMAND VERSION
    @commands.command(name="about")
    async def about_command(self, ctx):
        """Show information about the bot using prefix command"""
        try:
            # Just send a simple message first to confirm the command works
            embed = discord.Embed(
                title="🤖 About IndieGO Bot",
                description="Your Ultimate Development & Design Companion",
                color=EMBED_COLOR
            )
            embed.add_field(name="Version", value="1.0.0", inline=True)
            embed.add_field(name="Library", value=f"Discord.py {discord.__version__}", inline=True)
            embed.add_field(name="Uptime", value=self.get_bot_uptime(), inline=True)
            
            await ctx.send(embed=embed)
        except Exception as e:
            logger.error(f"Error in about command: {str(e)}")
            await ctx.send(f"Error: {str(e)}")

    # SUPER BASIC SLASH COMMAND VERSION
    @app_commands.command(name="about", description="Learn about the bot")
    async def about_slash(self, interaction: discord.Interaction):
        """Show information about the bot using slash command"""
        try:
            embed = discord.Embed(
                title="🤖 About IndieGO Bot",
                description="Your Ultimate Development & Design Companion",
                color=EMBED_COLOR
            )
            embed.add_field(name="Version", value="1.0.0", inline=True)
            embed.add_field(name="Library", value=f"Discord.py {discord.__version__}", inline=True)
            embed.add_field(name="Uptime", value=self.get_bot_uptime(), inline=True)
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            logger.error(f"Error in about slash command: {str(e)}")
            await interaction.response.send_message(f"Error: {str(e)}")

    @commands.command(name="choose")
    async def choose_command(self, ctx, *choices: str):
        """Choose between multiple options"""
        if not choices:
            await ctx.send("You need to provide some choices!")
            return
        choice = random.choice(choices)
        await ctx.send(f"I choose: {choice}")

    @app_commands.command(name="choose", description="Choose between multiple options")
    async def choose_slash(self, interaction: discord.Interaction, option1: str, option2: str = None, option3: str = None):
        """Choose between multiple options"""
        choices = [option1]
        if option2:
            choices.append(option2)
        if option3:
            choices.append(option3)
            
        choice = random.choice(choices)
        await interaction.response.send_message(f"I choose: {choice}")

    @commands.command(name="serverinfo")
    async def serverinfo_command(self, ctx):
        """Show information about the server"""
        guild = ctx.guild
        embed = discord.Embed(
            title=f"Server Info - {guild.name}",
            description=f"Information about the server {guild.name}",
            color=discord.Color.blue()
        )
        embed.add_field(name="Server ID", value=guild.id, inline=False)
        embed.add_field(name="Owner", value=guild.owner, inline=False)
        embed.add_field(name="Members", value=guild.member_count, inline=False)
        embed.add_field(name="Created At", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        await ctx.send(embed=embed)

    @app_commands.command(name="serverinfo", description="Show information about the server")
    async def serverinfo_slash(self, interaction: discord.Interaction):
        """Show information about the server"""
        guild = interaction.guild
        embed = discord.Embed(
            title=f"Server Info - {guild.name}",
            description=f"Information about the server {guild.name}",
            color=discord.Color.blue()
        )
        embed.add_field(name="Server ID", value=guild.id, inline=False)
        embed.add_field(name="Owner", value=guild.owner, inline=False)
        embed.add_field(name="Members", value=guild.member_count, inline=False)
        embed.add_field(name="Created At", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        await interaction.response.send_message(embed=embed)

    @commands.command(name="support")
    async def support_command(self, ctx):
        """Get the link to the support server"""
        embed = discord.Embed(
            title="Support Server",
            description=f"If you need help or have any questions, join our support server: [Support Server]({SUPPORT_SERVER_LINK})",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @app_commands.command(name="support", description="Get the link to the support server")
    async def support_slash(self, interaction: discord.Interaction):
        """Get the link to the support server"""
        embed = discord.Embed(
            title="Support Server",
            description=f"If you need help or have any questions, join our support server: [Support Server]({SUPPORT_SERVER_LINK})",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)

    @commands.command(name="profile")
    async def profile_command(self, ctx, member: discord.Member = None):
        """Show profile options for the user"""
        if member is None:
            member = ctx.author
        view = ProfileView(member)
        embed = discord.Embed(
            title=f"Profile - {member.name}",
            description="Click the buttons below to view different profile aspects.",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=member.avatar.url)
        await ctx.send(embed=embed, view=view)

    @app_commands.command(name="profile", description="Show profile options for the user")
    async def profile_slash(self, interaction: discord.Interaction, member: discord.Member = None):
        """Show profile options for the user"""
        if member is None:
            member = interaction.user
        view = ProfileView(member)
        embed = discord.Embed(
            title=f"Profile - {member.name}",
            description="Click the buttons below to view different profile aspects.",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=member.avatar.url)
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    """Set up the General cog"""
    cog = General(bot)
    await bot.add_cog(cog)
    
    # Force sync commands to test guild
    try:
        # Copy global commands to guild
        bot.tree.copy_global_to(guild=discord.Object(id=TEST_GUILD_IDS[0]))
        
        # Sync commands to guild
        await bot.tree.sync(guild=discord.Object(id=TEST_GUILD_IDS[0]))
        logger.info(f"Successfully synced commands to test guild {TEST_GUILD_IDS[0]}")
    except Exception as e:
        logger.error(f"Failed to sync commands to test guild: {str(e)}")
    
    logger.info("General cog setup complete")