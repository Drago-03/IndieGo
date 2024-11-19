import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta
import json

OWNER_ID = 950609706760691752

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.premium_users = {}
        self.team_members = [OWNER_ID]

    @commands.Cog.listener()
    async def on_ready(self):
        # Load premium users from file
        try:
            with open('premium_users.json', 'r') as f:
                self.premium_users = json.load(f)
        except FileNotFoundError:
            self.premium_users = {}

    def save_premium_users(self):
        with open('premium_users.json', 'w') as f:
            json.dump(self.premium_users, f)

    @app_commands.command(name="gift", description="Gift a premium tier to a user for a month")
    async def gift(self, interaction: discord.Interaction, tier: str, user_id: int):
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        if tier not in ["pro", "team", "enterprise"]:
            await interaction.response.send_message("Invalid tier. Choose from 'pro', 'team', or 'enterprise'.", ephemeral=True)
            return

        end_date = datetime.now() + timedelta(days=30)
        self.premium_users[user_id] = {"tier": tier, "end_date": end_date.isoformat()}
        self.save_premium_users()
        await interaction.response.send_message(f"Gifted {tier} tier to user {user_id} for a month.", ephemeral=True)

    @app_commands.command(name="team", description="Add a team member")
    async def team(self, interaction: discord.Interaction, user_id: int):
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        self.team_members.append(user_id)
        await interaction.response.send_message(f"Added user {user_id} to the team.", ephemeral=True)

    @app_commands.command(name="about", description="Show information about the bot")
    async def about(self, interaction: discord.Interaction):
        if interaction.user.id not in self.team_members:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        embed = discord.Embed(
            title="About IndieGO Bot",
            description="The ultimate Discord bot for developer communities!",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="Creator",
            value="Drago (drago.exe)",
            inline=False
        )
        embed.add_field(
            name="Support Server",
            value="[Join Support Server](https://discord.gg/9bPsjgnJ5v)",
            inline=False
        )
        embed.add_field(
            name="Website",
            value="https://your-private-website.com",
            inline=False
        )
        embed.add_field(
            name="Team Members",
            value="\n".join([f"<@{member_id}>" for member_id in self.team_members]),
            inline=False
        )
        embed.set_footer(text="IndieGO Bot", icon_url=self.bot.user.avatar.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ping", description="Check the bot's latency")
    async def ping(self, interaction: discord.Interaction):
        latency = self.bot.latency * 1000  # Convert to milliseconds
        await interaction.response.send_message(f"Pong! Latency: {latency:.2f} ms", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Admin(bot))