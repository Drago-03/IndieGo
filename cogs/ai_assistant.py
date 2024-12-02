import discord
from discord.ext import commands
from discord import app_commands
import anthropic
import google.generativeai as genai
import os
from typing import Optional
import asyncio
import aiohttp
from datetime import datetime, timedelta
import json

class AIAssistant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Initialize API keys from environment variables
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        
        # Initialize API clients
        if self.anthropic_api_key:
            self.claude = anthropic.Client(api_key=self.anthropic_api_key)
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
        
        # Rate limiting
        self.cooldowns = {}
        self.COOLDOWN_MINUTES = 1
        
        # Message history
        self.message_history = {}

    async def fetch_claude_response(self, prompt):
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

    @commands.command(name="ask")
    async def ask_command(self, ctx, *, question: str):
        """Ask a question to the AI assistant"""
        if ctx.author.id in self.cooldowns and self.cooldowns[ctx.author.id] > datetime.now():
            await ctx.send("You are on cooldown. Please wait before asking another question.")
            return

        prompt = f"User: {question}\nBot:"
        claude_response = await self.fetch_claude_response(prompt)
        gemini_response = await self.fetch_gemini_response(prompt)
        response = f"Claude: {claude_response}\nGemini: {gemini_response}"
        await ctx.send(response)

        self.cooldowns[ctx.author.id] = datetime.now() + timedelta(minutes=self.COOLDOWN_MINUTES)

    @app_commands.command(name="ask", description="Ask a question to the AI assistant")
    async def ask_slash(self, interaction: discord.Interaction, question: str):
        """Ask a question to the AI assistant"""
        if interaction.user.id in self.cooldowns and self.cooldowns[interaction.user.id] > datetime.now():
            await interaction.response.send_message("You are on cooldown. Please wait before asking another question.", ephemeral=True)
            return

        prompt = f"User: {question}\nBot:"
        claude_response = await self.fetch_claude_response(prompt)
        gemini_response = await self.fetch_gemini_response(prompt)
        response = f"Claude: {claude_response}\nGemini: {gemini_response}"
        await interaction.response.send_message(response)

        self.cooldowns[interaction.user.id] = datetime.now() + timedelta(minutes=self.COOLDOWN_MINUTES)

async def setup(bot):
    await bot.add_cog(AIAssistant(bot))