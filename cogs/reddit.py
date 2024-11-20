import discord
from discord.ext import commands
import praw
import random
import os

class Reddit(commands.Cog):
    """Cog for Reddit integration"""

    def __init__(self, bot):
        self.bot = bot
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent="discord:indiego_bot:v1.0 (by u/your_reddit_username)"
        )

    @commands.command(name="meme")
    async def meme_command(self, ctx):
        """Fetch a programming meme from Reddit"""
        subreddit = self.reddit.subreddit("ProgrammerHumor")
        posts = [post for post in subreddit.hot(limit=50) if not post.stickied]
        post = random.choice(posts)
        embed = discord.Embed(title=post.title, url=post.url)
        embed.set_image(url=post.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Reddit(bot))