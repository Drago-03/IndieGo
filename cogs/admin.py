import discord
from discord.ext import commands
from discord import app_commands
import json
from datetime import datetime, timedelta

OWNER_ID = 950609706760691752  # Replace with your Discord ID

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

    @commands.command(name="gift")
    async def gift_command(self, ctx, tier: str, user_id: int):
        """Gift a premium tier to a user for a month"""
        if ctx.author.id != OWNER_ID:
            await ctx.send("You do not have permission to use this command.")
            return

        if tier not in ["pro", "team", "enterprise"]:
            await ctx.send("Invalid tier. Choose from 'pro', 'team', or 'enterprise'.")
            return

        end_date = datetime.now() + timedelta(days=30)
        self.premium_users[user_id] = {"tier": tier, "end_date": end_date.isoformat()}
        self.save_premium_users()
        await ctx.send(f"Gifted {tier} tier to user {user_id} for a month.")

    @app_commands.command(name="gift", description="Gift a premium tier to a user for a month")
    async def gift(self, interaction: discord.Interaction, tier: str, user_id: int):
        """Gift a premium tier to a user for a month"""
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

    @commands.command(name="team")
    async def team_command(self, ctx, user_id: int):
        """Add a team member"""
        if ctx.author.id != OWNER_ID:
            await ctx.send("You do not have permission to use this command.")
            return

        self.team_members.append(user_id)
        await ctx.send(f"Added user {user_id} to the team.")

    @app_commands.command(name="team", description="Add a team member")
    async def team(self, interaction: discord.Interaction, user_id: int):
        """Add a team member"""
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        self.team_members.append(user_id)
        await interaction.response.send_message(f"Added user {user_id} to the team.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Admin(bot))