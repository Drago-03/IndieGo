import discord
from discord.ext import commands
import requests

class Reddit(commands.Cog):
    """Cog for Reddit integration"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="meme")
    async def meme_command(self, ctx):
        """Fetch a programming meme from Reddit"""
        response = requests.get("https://meme-api.com/gimme/ProgrammerHumor")
        if response.status_code == 200:
            data = response.json()
            embed = discord.Embed(title=data['title'], url=data['postLink'], color=discord.Color.blue())
            embed.set_image(url=data['url'])
            embed.set_footer(text=f"👍 {data['ups']} | 💬 {data['num_comments']}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("Failed to fetch a meme. Please try again later.")

async def setup(bot):
    await bot.add_cog(Reddit(bot))