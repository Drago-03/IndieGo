import discord
from discord.ext import commands
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx, dice: str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
            result = [random.randint(1, limit) for r in range(rolls)]
            await ctx.send(f'Results: {", ".join(map(str, result))}')
        except Exception:
            await ctx.send('Format has to be in NdN!')

    @commands.command()
    async def choose(self, ctx, *choices: str):
        """Chooses between multiple choices."""
        await ctx.send(random.choice(choices))

    @commands.command()
    async def poll(self, ctx, question, *options):
        """Creates a poll with reactions."""
        if len(options) > 10:
            await ctx.send('You can only have up to 10 options!')
            return

        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        
        description = []
        for i, option in enumerate(options):
            description.append(f'{reactions[i]} {option}')
        
        embed = discord.Embed(title=question, description='\n'.join(description))
        react_message = await ctx.send(embed=embed)
        
        for i in range(len(options)):
            await react_message.add_reaction(reactions[i])

    @commands.command()
    async def joke(self, ctx):
        """Tells a programming joke."""
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "Why do Python programmers wear glasses? Because they can't C!",
            "What's a programmer's favorite place? The foo bar!",
            "Why did the programmer quit his job? Because he didn't get arrays!",
            "What do you call a programmer from Finland? Nerdic!"
        ]
        await ctx.send(random.choice(jokes))

async def setup(bot):
    await bot.add_cog(Fun(bot))