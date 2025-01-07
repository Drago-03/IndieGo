import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import os

class AIAssistant(commands.Cog):
    """AI-Developer Assistance commands"""

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

    @commands.command(name="ask")
    async def ask_command(self, ctx, *, question: str):
        """Ask a general question to the AI assistant"""
        try:
            prompt = f"Answer the following question:\n{question}"
            answer = await self.generate_response(prompt)
            await ctx.send(answer)
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

    @app_commands.command(name="ask", description="Ask a general question to the AI assistant")
    async def ask_slash(self, interaction: discord.Interaction, question: str):
        """Ask a general question to the AI assistant"""
        try:
            prompt = f"Answer the following question:\n{question}"
            answer = await self.generate_response(prompt)
            await interaction.response.send_message(answer)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @commands.command(name="codehelp")
    async def codehelp_command(self, ctx, *, code: str):
        """Get coding help using multiple AI models"""
        try:
            prompt = f"Provide help for the following code:\n{code}"
            help_response = await self.generate_response(prompt)
            await ctx.send(help_response)
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

    @app_commands.command(name="codehelp", description="Get coding help using multiple AI models")
    async def codehelp_slash(self, interaction: discord.Interaction, code: str):
        """Get coding help using multiple AI models"""
        try:
            prompt = f"Provide help for the following code:\n{code}"
            help_response = await self.generate_response(prompt)
            await interaction.response.send_message(help_response)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

async def setup(bot):
    await bot.add_cog(AIAssistant(bot))