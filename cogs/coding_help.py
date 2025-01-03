import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import os

class CodingHelp(commands.Cog):
    """Cog for providing coding help using AI"""

    def __init__(self, bot):
        self.bot = bot
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')

    async def generate_response(self, prompt):
        async with aiohttp.ClientSession() as session:
            headers = {
                'Authorization': f'Bearer {self.anthropic_api_key}',
                'Content-Type': 'application/json'
            }
            data = {
                'prompt': prompt,
                'max_tokens': 150
            }
            async with session.post('https://api.anthropic.com/v1/complete', headers=headers, json=data) as response:
                result = await response.json()
                claude_response = result['choices'][0]['text']

            headers = {
                'Authorization': f'Bearer {self.gemini_api_key}',
                'Content-Type': 'application/json'
            }
            async with session.post('https://api.gemini.com/v1/complete', headers=headers, json=data) as response:
                result = await response.json()
                gemini_response = result['choices'][0]['text']

        return f"Claude: {claude_response}\nGemini: {gemini_response}"

    @commands.command(name="debug")
    async def debug_command(self, ctx, *, code: str):
        """Help debug code issues"""
        try:
            prompt = f"Debug the following code:\n{code}"
            answer = await self.generate_response(prompt)
            await ctx.send(answer)
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

    @commands.command(name="optimize")
    async def optimize_command(self, ctx, *, code: str):
        """Suggest code optimizations"""
        try:
            prompt = f"Optimize the following code:\n{code}"
            answer = await self.generate_response(prompt)
            await ctx.send(answer)
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

    @app_commands.command(name="debug", description="Help debug code issues")
    async def debug_slash(self, interaction: discord.Interaction, code: str):
        """Help debug code issues"""
        try:
            prompt = f"Debug the following code:\n{code}"
            answer = await self.generate_response(prompt)
            await interaction.response.send_message(answer)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @app_commands.command(name="optimize", description="Suggest code optimizations")
    async def optimize_slash(self, interaction: discord.Interaction, code: str):
        """Suggest code optimizations"""
        try:
            prompt = f"Optimize the following code:\n{code}"
            answer = await self.generate_response(prompt)
            await interaction.response.send_message(answer)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

async def setup(bot):
    await bot.add_cog(CodingHelp(bot))