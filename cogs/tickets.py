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

    @app_commands.command(name="ticket", description="Creates a ticket.")
    async def ticket(self, interaction: discord.Interaction, reason: str = None):
        if not reason:
            return await interaction.response.send_message("Please provide a reason for creating a ticket!")

        category = self.bot.get_channel(TICKET_CATEGORY_ID)
        if not category:
            return await interaction.response.send_message("Ticket category not configured!")

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
                return await interaction.response.send_message("You do not have permission to close this ticket.", ephemeral=True)

            await channel.delete()
            log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
            log_embed = discord.Embed(title="Ticket Closed", description=f"Ticket created by {interaction.user.mention}\nReason: {reason}\nClosed by: {interaction.user.mention}", color=discord.Color.red())
            await log_channel.send(embed=log_embed)
            await interaction.user.send(f"Your ticket has been closed. Reason: {reason}")

        close_button.callback = close_ticket

        await channel.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Tickets(bot))