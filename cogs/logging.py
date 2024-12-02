import discord
from discord.ext import commands
from discord import app_commands

class Logging(commands.Cog):
    """Cog for logging actions and errors"""

    def __init__(self, bot):
        self.bot = bot
        self.log_category = None
        self.log_channels = {}

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.guilds[0]
        self.log_category = discord.utils.get(guild.categories, name="Server Logging")
        if not self.log_category:
            self.log_category = await guild.create_category("Server Logging")

        log_channel_names = ["admin-logs", "server-logs"]
        for name in log_channel_names:
            try:
                channel = discord.utils.get(guild.text_channels, name=name)
                if not channel:
                    channel = await guild.create_text_channel(name, category=self.log_category)
                self.log_channels[name] = channel
            except Exception as e:
                print(f"Failed to create or get channel {name}: {e}")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.display_name != after.display_name:
            embed = discord.Embed(
                title="Nickname Changed",
                description=f"{before.mention} changed their nickname.",
                color=discord.Color.blue()
            )
            embed.add_field(name="Before", value=before.display_name, inline=True)
            embed.add_field(name="After", value=after.display_name, inline=True)
            await self.log_channels["server-logs"].send(embed=embed)

        if before.roles != after.roles:
            embed = discord.Embed(
                title="Roles Updated",
                description=f"{before.mention} had their roles updated.",
                color=discord.Color.blue()
            )
            before_roles = ", ".join([role.name for role in before.roles])
            after_roles = ", ".join([role.name for role in after.roles])
            embed.add_field(name="Before", value=before_roles, inline=True)
            embed.add_field(name="After", value=after_roles, inline=True)
            await self.log_channels["server-logs"].send(embed=embed)

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if before.avatar != after.avatar:
            embed = discord.Embed(
                title="Avatar Changed",
                description=f"{before.mention} changed their avatar.",
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=before.avatar.url)
            embed.set_image(url=after.avatar.url)
            await self.log_channels["server-logs"].send(embed=embed)

        if before.name != after.name:
            embed = discord.Embed(
                title="Username Changed",
                description=f"{before.mention} changed their username.",
                color=discord.Color.blue()
            )
            embed.add_field(name="Before", value=before.name, inline=True)
            embed.add_field(name="After", value=after.name, inline=True)
            await self.log_channels["server-logs"].send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(
            title="Member Joined",
            description=f"{member.mention} joined the server.",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=member.avatar.url)
        await self.log_channels["server-logs"].send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = discord.Embed(
            title="Member Left",
            description=f"{member.mention} left the server.",
            color=discord.Color.red()
        )
        await self.log_channels["server-logs"].send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        embed = discord.Embed(
            title="Command Error",
            description=f"An error occurred: {error}",
            color=discord.Color.red()
        )
        await self.log_channels["admin-logs"].send(embed=embed)

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        embed = discord.Embed(
            title="Command Executed",
            description=f"{ctx.command} was executed by {ctx.author.mention}.",
            color=discord.Color.green()
        )
        await self.log_channels["admin-logs"].send(embed=embed)

    @commands.command(name="setup_logs")
    @commands.has_permissions(administrator=True)
    async def setup_logs_command(self, ctx):
        """Setup logging channels"""
        guild = ctx.guild
        self.log_category = discord.utils.get(guild.categories, name="Server Logging")
        if not self.log_category:
            self.log_category = await guild.create_category("Server Logging")

        log_channel_names = ["admin-logs", "server-logs"]
        for name in log_channel_names:
            try:
                channel = discord.utils.get(guild.text_channels, name=name)
                if not channel:
                    channel = await guild.create_text_channel(name, category=self.log_category)
                self.log_channels[name] = channel
            except Exception as e:
                await ctx.send(f"Failed to create or get channel {name}: {e}")
                return

        await ctx.send("Logging channels setup successfully.")

    @app_commands.command(name="setup_logs", description="Setup logging channels")
    @commands.has_permissions(administrator=True)
    async def setup_logs(self, interaction: discord.Interaction):
        """Setup logging channels"""
        guild = interaction.guild
        self.log_category = discord.utils.get(guild.categories, name="Server Logging")
        if not self.log_category:
            self.log_category = await guild.create_category("Server Logging")

        log_channel_names = ["admin-logs", "server-logs"]
        for name in log_channel_names:
            try:
                channel = discord.utils.get(guild.text_channels, name=name)
                if not channel:
                    channel = await guild.create_text_channel(name, category=self.log_category)
                self.log_channels[name] = channel
            except Exception as e:
                await interaction.response.send_message(f"Failed to create or get channel {name}: {e}", ephemeral=True)
                return

        await interaction.response.send_message("Logging channels setup successfully.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Logging(bot))