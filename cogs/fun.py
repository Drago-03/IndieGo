import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="roll", description="Rolls a dice in NdN format.")
    async def roll(self, interaction: discord.Interaction, dice: str):
        try:
            rolls, limit = map(int, dice.split('d'))
            result = [random.randint(1, limit) for r in range(rolls)]
            await interaction.response.send_message(f'Results: {", ".join(map(str, result))}')
        except Exception:
            await interaction.response.send_message('Format has to be in NdN!')

    @app_commands.command(name="choose", description="Chooses between multiple choices.")
    async def choose(self, interaction: discord.Interaction, *choices: str):
        await interaction.response.send_message(random.choice(choices))

    @app_commands.command(name="poll", description="Creates a poll with reactions.")
    async def poll(self, interaction: discord.Interaction, question: str, *options: str):
        if len(options) > 10:
            await interaction.response.send_message('You can only have up to 10 options!')
            return

        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        
        description = []
        for i, option in enumerate(options):
            description.append(f'{reactions[i]} {option}')
        
        embed = discord.Embed(title=question, description='\n'.join(description))
        poll_message = await interaction.response.send_message(embed=embed)
        
        for i in range(len(options)):
            await poll_message.add_reaction(reactions[i])

    @app_commands.command(name="trivia", description="Starts a trivia game with programming questions.")
    async def trivia(self, interaction: discord.Interaction):
        questions = [
            {"question": "What does HTML stand for?", "answer": "HyperText Markup Language"},
            {"question": "What is the main programming language used for Android development?", "answer": "Java"},
            {"question": "What does CSS stand for?", "answer": "Cascading Style Sheets"},
            {"question": "What is the name of the Python package manager?", "answer": "pip"},
            {"question": "What is the main language used for web development?", "answer": "JavaScript"}
        ]
        question = random.choice(questions)
        await interaction.response.send_message(question["question"])

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            answer = await self.bot.wait_for('message', check=check, timeout=15.0)
        except asyncio.TimeoutError:
            return await interaction.followup.send(f'Sorry, you took too long. The correct answer was {question["answer"]}.')

        if answer.content.lower() == question["answer"].lower():
            await interaction.followup.send('Correct!')
        else:
            await interaction.followup.send(f'Incorrect. The correct answer was {question["answer"]}.')

    @app_commands.command(name="codechallenge", description="Gives a random coding challenge.")
    async def codechallenge(self, interaction: discord.Interaction):
        challenges = [
            "Write a function that reverses a string.",
            "Write a function that checks if a number is prime.",
            "Write a function that sorts a list of numbers.",
            "Write a function that finds the factorial of a number.",
            "Write a function that checks if a string is a palindrome."
        ]
        challenge = random.choice(challenges)
        await interaction.response.send_message(f'Your coding challenge is: {challenge}')

    @app_commands.command(name="quote", description="Sends a random inspirational quote.")
    async def quote(self, interaction: discord.Interaction):
        quotes = [
            "Code is like humor. When you have to explain it, it’s bad. – Cory House",
            "Fix the cause, not the symptom. – Steve Maguire",
            "Optimism is an occupational hazard of programming: feedback is the treatment. – Kent Beck",
            "When to use iterative development? You should use iterative development only on projects that you want to succeed. – Martin Fowler",
            "Simplicity is the soul of efficiency. – Austin Freeman"
        ]
        quote = random.choice(quotes)
        await interaction.response.send_message(quote)

    @app_commands.command(name="joke", description="Tells a random programming joke.")
    async def joke(self, interaction: discord.Interaction):
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "Why do Java developers wear glasses? Because they don't see sharp.",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
            "Why do Python programmers have low self-esteem? Because they're constantly comparing their self to others.",
            "Why do programmers hate nature? It has too many bugs."
        ]
        joke = random.choice(jokes)
        await interaction.response.send_message(joke)

async def setup(bot):
    await bot.add_cog(Fun(bot))