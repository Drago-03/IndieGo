import discord
from discord.ext import commands
import random
import asyncio

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
        poll_message = await ctx.send(embed=embed)
        
        for i in range(len(options)):
            await poll_message.add_reaction(reactions[i])

    @commands.command()
    async def trivia(self, ctx):
        """Starts a trivia game with programming questions."""
        questions = [
            {"question": "What does HTML stand for?", "answer": "HyperText Markup Language"},
            {"question": "What is the main programming language used for Android development?", "answer": "Java"},
            {"question": "What does CSS stand for?", "answer": "Cascading Style Sheets"},
            {"question": "What is the name of the Python package manager?", "answer": "pip"},
            {"question": "What is the main language used for web development?", "answer": "JavaScript"}
        ]
        question = random.choice(questions)
        await ctx.send(question["question"])

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            answer = await self.bot.wait_for('message', check=check, timeout=15.0)
        except asyncio.TimeoutError:
            return await ctx.send(f'Sorry, you took too long. The correct answer was {question["answer"]}.')

        if answer.content.lower() == question["answer"].lower():
            await ctx.send('Correct!')
        else:
            await ctx.send(f'Incorrect. The correct answer was {question["answer"]}.')

    @commands.command()
    async def codechallenge(self, ctx):
        """Gives a random coding challenge."""
        challenges = [
            "Write a function that reverses a string.",
            "Write a function that checks if a number is prime.",
            "Write a function that sorts a list of numbers.",
            "Write a function that finds the factorial of a number.",
            "Write a function that checks if a string is a palindrome."
        ]
        challenge = random.choice(challenges)
        await ctx.send(f'Your coding challenge is: {challenge}')

    @commands.command()
    async def quote(self, ctx):
        """Sends a random inspirational quote."""
        quotes = [
            "Code is like humor. When you have to explain it, it’s bad. – Cory House",
            "Fix the cause, not the symptom. – Steve Maguire",
            "Optimism is an occupational hazard of programming: feedback is the treatment. – Kent Beck",
            "When to use iterative development? You should use iterative development only on projects that you want to succeed. – Martin Fowler",
            "Simplicity is the soul of efficiency. – Austin Freeman"
        ]
        quote = random.choice(quotes)
        await ctx.send(quote)

    @commands.command()
    async def joke(self, ctx):
        """Tells a random programming joke."""
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "Why do Java developers wear glasses? Because they don't see sharp.",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
            "Why do Python programmers have low self-esteem? Because they're constantly comparing their self to others.",
            "Why do programmers hate nature? It has too many bugs."
        ]
        joke = random.choice(jokes)
        await ctx.send(joke)

async def setup(bot):
    await bot.add_cog(Fun(bot))