import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
import random

SUPPORT_SERVER_LINK = "https://discord.gg/your-support-server-link"

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

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping_command(self, ctx):
        """Check the bot's latency"""
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

    @app_commands.command(name="ping", description="Check the bot's latency")
    async def ping(self, interaction: discord.Interaction):
        """Check the bot's latency"""
        await interaction.response.send_message(f"Pong! {round(self.bot.latency * 1000)}ms")

    @commands.command(name="about")
    async def about_command(self, ctx):
        """Show information about the bot"""
        embed = discord.Embed(
            title="About IndieGO Bot",
            description="IndieGO is a powerful, all-in-one Discord bot designed for developers. It offers moderation tools, ticket creation, and coding assistance, along with fun utilities.",
            color=discord.Color.blue()
        )
        embed.add_field(name="Author", value="Drago", inline=False)
        embed.add_field(name="Website", value="[IndieGO Website](https://drago-03.github.io/IndieGo-Website/)", inline=False)
        embed.set_footer(text="Thank you for using IndieGO Bot!")
        await ctx.send(embed=embed)

    @app_commands.command(name="about", description="Show information about the bot")
    async def about(self, interaction: discord.Interaction):
        """Show information about the bot"""
        embed = discord.Embed(
            title="About IndieGO Bot",
            description="IndieGO is a powerful, all-in-one Discord bot designed for developers. It offers moderation tools, ticket creation, and coding assistance, along with fun utilities.",
            color=discord.Color.blue()
        )
        embed.add_field(name="Author", value="Drago", inline=False)
        embed.add_field(name="Website", value="[IndieGO Website](https://drago-03.github.io/IndieGo-Website/)", inline=False)
        embed.set_footer(text="Thank you for using IndieGO Bot!")
        await interaction.response.send_message(embed=embed)

    @commands.command(name="choose")
    async def choose_command(self, ctx, *choices: str):
        """Choose between multiple options"""
        if not choices:
            await ctx.send("You need to provide some choices!")
            return
        choice = random.choice(choices)
        await ctx.send(f"I choose: {choice}")

    @app_commands.command(name="choose", description="Choose between multiple options")
    async def choose(self, interaction: discord.Interaction, *choices: str):
        """Choose between multiple options"""
        if not choices:
            await interaction.response.send_message("You need to provide some choices!", ephemeral=True)
            return
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
        embed.add_field(name="Region", value=guild.region, inline=False)
        embed.add_field(name="Members", value=guild.member_count, inline=False)
        embed.add_field(name="Created At", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        await ctx.send(embed=embed)

    @app_commands.command(name="serverinfo", description="Show information about the server")
    async def serverinfo(self, interaction: discord.Interaction):
        """Show information about the server"""
        guild = interaction.guild
        embed = discord.Embed(
            title=f"Server Info - {guild.name}",
            description=f"Information about the server {guild.name}",
            color=discord.Color.blue()
        )
        embed.add_field(name="Server ID", value=guild.id, inline=False)
        embed.add_field(name="Owner", value=guild.owner, inline=False)
        embed.add_field(name="Region", value=guild.region, inline=False)
        embed.add_field(name="Members", value=guild.member_count, inline=False)
        embed.add_field(name="Created At", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
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
    async def support(self, interaction: discord.Interaction):
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
        await ctx.send("Choose an option:", view=view)

    @app_commands.command(name="profile", description="Show profile options for the user")
    async def profile(self, interaction: discord.Interaction, member: discord.Member = None):
        """Show profile options for the user"""
        if member is None:
            member = interaction.user
        view = ProfileView(member)
        await interaction.response.send_message("Choose an option:", view=view)

async def setup(bot):
    await bot.add_cog(General(bot))