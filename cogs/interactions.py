import discord
from discord.ext import commands
import aiohttp
import os

class InteractiveDM(commands.Cog):
    """Cog for handling interactive DM interactions"""

    def __init__(self, bot):
        self.bot = bot
        self.claude_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')

    async def fetch_claude_response(self, prompt):
        async with aiohttp.ClientSession() as session:
            headers = {
                'Authorization': f'Bearer {self.claude_api_key}',
                'Content-Type': 'application/json'
            }
            data = {
                'prompt': prompt,
                'max_tokens': 150
            }
            async with session.post('https://api.anthropic.com/v1/complete', headers=headers, json=data) as response:
                result = await response.json()
                return result['choices'][0]['text']

    async def fetch_gemini_response(self, prompt):
        async with aiohttp.ClientSession() as session:
            headers = {
                'Authorization': f'Bearer {self.gemini_api_key}',
                'Content-Type': 'application/json'
            }
            data = {
                'prompt': prompt,
                'max_tokens': 150
            }
            async with session.post('https://api.gemini.com/v1/complete', headers=headers, json=data) as response:
                result = await response.json()
                return result['choices'][0]['text']

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if self.bot.user in message.mentions or message.reference:
            prompt = f"User: {message.content}\nBot (as a nerdy human):"
            claude_response = await self.fetch_claude_response(prompt)
            gemini_response = await self.fetch_gemini_response(prompt)
            response = f"Claude: {claude_response}\nGemini: {gemini_response}"
            await message.channel.send(response)

async def setup(bot):
    await bot.add_cog(InteractiveDM(bot))