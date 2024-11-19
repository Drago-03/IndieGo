import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roll")
    async def roll_command(self, ctx, dice: str = None):
        """Rolls a dice in NdN format."""
        if dice is None:
            embed = discord.Embed(
                title="Error",
                description="You must specify the dice format (e.g., 2d6).",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        try:
            rolls, limit = map(int, dice.split('d'))
            result = [random.randint(1, limit) for r in range(rolls)]
            embed = discord.Embed(
                title="Dice Roll",
                description=f'Results: {", ".join(map(str, result))}',
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        except Exception:
            embed = discord.Embed(
                title="Error",
                description="Format has to be in NdN!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @app_commands.command(name="roll", description="Rolls a dice in NdN format.")
    async def roll(self, interaction: discord.Interaction, dice: str = None):
        """Rolls a dice in NdN format."""
        if dice is None:
            embed = discord.Embed(
                title="Error",
                description="You must specify the dice format (e.g., 2d6).",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        try:
            rolls, limit = map(int, dice.split('d'))
            result = [random.randint(1, limit) for r in range(rolls)]
            embed = discord.Embed(
                title="Dice Roll",
                description=f'Results: {", ".join(map(str, result))}',
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed)
        except Exception:
            embed = discord.Embed(
                title="Error",
                description="Format has to be in NdN!",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.command(name="choose")
    async def choose_command(self, ctx, *, choices: str = None):
        """Chooses between multiple choices."""
        if choices is None:
            embed = discord.Embed(
                title="Error",
                description="You must specify choices separated by commas.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        choices_list = choices.split(',')
        choice = random.choice(choices_list)
        embed = discord.Embed(
            title="Choice",
            description=f'I choose: {choice.strip()}',
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @app_commands.command(name="choose", description="Chooses between multiple choices.")
    async def choose(self, interaction: discord.Interaction, choices: str = None):
        """Chooses between multiple choices."""
        if choices is None:
            embed = discord.Embed(
                title="Error",
                description="You must specify choices separated by commas.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        choices_list = choices.split(',')
        choice = random.choice(choices_list)
        embed = discord.Embed(
            title="Choice",
            description=f'I choose: {choice.strip()}',
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

    @commands.command(name="poll")
    async def poll_command(self, ctx, question: str = None, *, options: str = None):
        """Creates a poll with reactions."""
        if question is None or options is None:
            embed = discord.Embed(
                title="Error",
                description="You must specify a question and options.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        options_list = options.split(',')
        if len(options_list) > 10:
            embed = discord.Embed(
                title="Error",
                description="You can only have up to 10 options!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        
        description = []
        for i, option in enumerate(options_list):
            description.append(f'{reactions[i]} {option}')
        
        embed = discord.Embed(title=question, description='\n'.join(description), color=discord.Color.blue())
        poll_message = await ctx.send(embed=embed)
        
        for i in range(len(options_list)):
            await poll_message.add_reaction(reactions[i])

    @app_commands.command(name="poll", description="Create a poll")
    async def poll(self, interaction: discord.Interaction, question: str):
        """Create a poll"""
        embed = discord.Embed(
            title="Poll",
            description=question,
            color=discord.Color.blue()
        )
        message = await interaction.response.send_message(embed=embed)
        await message.add_reaction("👍")
        await message.add_reaction("👎")

    @commands.command(name="trivia")
    async def trivia_command(self, ctx):
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
            embed = discord.Embed(
                title="Timeout",
                description=f'Sorry, you took too long. The correct answer was {question["answer"]}.',
                color=discord.Color.red()
            )
            return await ctx.send(embed=embed)

        if answer.content.lower() == question["answer"].lower():
            embed = discord.Embed(
                title="Correct",
                description='Correct!',
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Incorrect",
                description=f'Incorrect. The correct answer was {question["answer"]}.',
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @app_commands.command(name="trivia", description="Start a trivia game")
    async def trivia(self, interaction: discord.Interaction):
        """Start a trivia game"""
        questions = [
            {"question": "What is the capital of France?", "answer": "Paris"},
            {"question": "What is 2 + 2?", "answer": "4"},
            {"question": "Who wrote 'To Kill a Mockingbird'?", "answer": "Harper Lee"}
        ]
        question = random.choice(questions)
        embed = discord.Embed(
            title="Trivia",
            description=question["question"],
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            answer = await self.bot.wait_for('message', check=check, timeout=15.0)
        except asyncio.TimeoutError:
            await interaction.followup.send(f'Time is up! The correct answer was {question["answer"]}.')
        else:
            if answer.content.lower() == question["answer"].lower():
                await interaction.followup.send('Correct!')
            else:
                await interaction.followup.send(f'Incorrect! The correct answer was {question["answer"]}.')

    @commands.command(name="codechallenge")
    async def codechallenge_command(self, ctx):
        """Gives a random coding challenge."""
        challenges = [
            "Write a function that reverses a string.",
            "Write a function that checks if a number is prime.",
            "Write a function that sorts a list of numbers.",
            "Write a function that finds the factorial of a number.",
            "Write a function that checks if a string is a palindrome."
        ]
        challenge = random.choice(challenges)
        embed = discord.Embed(
            title="Coding Challenge",
            description=f'Your coding challenge is: {challenge}',
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @commands.command(name="quote")
    async def quote_command(self, ctx):
        """Sends a random inspirational quote."""
        quotes = [
            "Code is like humor. When you have to explain it, it’s bad. – Cory House",
            "Fix the cause, not the symptom. – Steve Maguire",
            "Optimism is an occupational hazard of programming: feedback is the treatment. – Kent Beck",
            "When to use iterative development? You should use iterative development only on projects that you want to succeed. – Martin Fowler",
            "Simplicity is the soul of efficiency. – Austin Freeman"
        ]
        quote = random.choice(quotes)
        embed = discord.Embed(
            title="Inspirational Quote",
            description=quote,
            color=discord.Color.purple()
        )
        await ctx.send(embed=embed)

    @commands.command(name="joke")
    async def joke_command(self, ctx):
        """Tells a random programming joke."""
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "Why do Java developers wear glasses? Because they don't see sharp.",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
            "Why do Python programmers have low self-esteem? Because they're constantly comparing their self to others.",
            "Why do programmers hate nature? It has too many bugs."
        ]
        joke = random.choice(jokes)
        embed = discord.Embed(
            title="Programming Joke",
            description=joke,
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot))