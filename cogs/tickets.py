import discord
from discord.ext import commands
from config import TICKET_CATEGORY_ID, STAFF_ROLE_ID

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ticket(self, ctx, *, reason=None):
        if not reason:
            return await ctx.send("Please provide a reason for creating a ticket!")

        category = self.bot.get_channel(TICKET_CATEGORY_ID)
        if not category:
            return await ctx.send("Ticket category not configured!")

        channel_name = f"ticket-{ctx.author.name}-{ctx.author.discriminator}"
        
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            ctx.guild.get_role(STAFF_ROLE_ID): discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        channel = await ctx.guild.create_text_channel(
            name=channel_name,
            category=category,
            overwrites=overwrites
        )

        await channel.send(
            f"Ticket created by {ctx.author.mention}\n"
            f"Reason: {reason}\n"
            f"Staff will be with you shortly.\n"
            f"Use `!close` to close this ticket."
        )

    @commands.command()
    async def close(self, ctx):
        if not ctx.channel.name.startswith("ticket-"):
            return await ctx.send("This command can only be used in ticket channels!")
        
        await ctx.send("Closing ticket in 5 seconds...")
        await ctx.channel.delete(delay=5)

async def setup(bot):
    await bot.add_cog(Tickets(bot))