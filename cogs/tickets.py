import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import app_commands
from config import TICKET_CATEGORY_ID, STAFF_ROLE_ID, LOG_CHANNEL_ID

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.guilds[0]
        self.ticket_mod_role = discord.utils.get(guild.roles, name="IndieGO Ticket Mod")
        if not self.ticket_mod_role:
            self.ticket_mod_role = await guild.create_role(name="IndieGO Ticket Mod")

    @commands.command(name="ticket")
    async def ticket_command(self, ctx, *, reason: str = None):
        """Creates a ticket"""
        if not reason:
            await ctx.send("Please provide a reason for creating a ticket!")
            return

        category = self.bot.get_channel(TICKET_CATEGORY_ID)
        if not category:
            await ctx.send("Ticket category not configured!")
            return

        channel_name = f"ticket-{ctx.author.name}-{ctx.author.discriminator}"
        
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            self.ticket_mod_role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        channel = await ctx.guild.create_text_channel(
            name=channel_name,
            category=category,
            overwrites=overwrites
        )

        embed = discord.Embed(title="Ticket Created", description=f"Ticket created by {ctx.author.mention}\nReason: {reason}\nStaff will be with you shortly.\nUse the buttons below to interact with this ticket.", color=discord.Color.blue())
        close_button = Button(label="Close Ticket", style=discord.ButtonStyle.red)
        view = View()
        view.add_item(close_button)

        async def close_ticket(interaction):
            if interaction.user != ctx.author and not self.ticket_mod_role in interaction.user.roles:
                await interaction.response.send_message("You do not have permission to close this ticket.", ephemeral=True)
                return

            await channel.delete()
            await interaction.response.send_message("Ticket closed.", ephemeral=True)

        close_button.callback = close_ticket
        await channel.send(embed=embed, view=view)

    @app_commands.command(name="ticket", description="Creates a ticket.")
    async def ticket(self, interaction: discord.Interaction, reason: str = None):
        """Creates a ticket"""
        if not reason:
            await interaction.response.send_message("Please provide a reason for creating a ticket!")
            return

        category = self.bot.get_channel(TICKET_CATEGORY_ID)
        if not category:
            await interaction.response.send_message("Ticket category not configured!")
            return

        channel_name = f"ticket-{interaction.user.name}-{interaction.user.discriminator}"
        
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            self.ticket_mod_role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        channel = await interaction.guild.create_text_channel(
            name=channel_name,
            category=category,
            overwrites=overwrites
        )

        embed = discord.Embed(title="Ticket Created", description=f"Ticket created by {interaction.user.mention}\nReason: {reason}\nStaff will be with you shortly.\nUse the buttons below to interact with this ticket.", color=discord.Color.blue())
        close_button = Button(label="Close Ticket", style=discord.ButtonStyle.red)
        view = View()
        view.add_item(close_button)

        async def close_ticket(interaction):
            if interaction.user != interaction.user and not self.ticket_mod_role in interaction.user.roles:
                await interaction.response.send_message("You do not have permission to close this ticket.", ephemeral=True)
                return

            await channel.delete()
            await interaction.response.send_message("Ticket closed.", ephemeral=True)

        close_button.callback = close_ticket
        await channel.send(embed=embed, view=view)

    @commands.command(name="setup_logs")
    async def setup_logs_command(self, ctx):
        """Setup logging channels"""
        guild = ctx.guild
        self.log_category = discord.utils.get(guild.categories, name="Logs")
        if not self.log_category:
            self.log_category = await guild.create_category("Logs")

        log_channel_names = ["general-logs", "error-logs", "command-logs"]
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
    async def setup_logs(self, interaction: discord.Interaction):
        """Setup logging channels"""
        guild = interaction.guild
        self.log_category = discord.utils.get(guild.categories, name="Logs")
        if not self.log_category:
            self.log_category = await guild.create_category("Logs")

        log_channel_names = ["general-logs", "error-logs", "command-logs"]
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
    await bot.add_cog(Tickets(bot))