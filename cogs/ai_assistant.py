import discord
from discord.ext import commands
from discord import app_commands
import openai
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
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        
        # Initialize API clients
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        if self.anthropic_api_key:
            self.claude = anthropic.Client(api_key=self.anthropic_api_key)
        if self.google_api_key:
            genai.configure(api_key=self.google_api_key)
        
        # Rate limiting
        self.cooldowns = {}
        self.COOLDOWN_MINUTES = 1
        
        # Message history
        self.conversation_history = {}

    async def get_ai_response(self, prompt: str, user_id: str, model: str = "gpt-3.5-turbo") -> str:
        """Generate AI response using available models"""
        try:
            # Check cooldown
            if not await self.check_cooldown(user_id):
                return "Please wait a moment before making another request."

            # Handle different AI services
            if self.openai_api_key and model.startswith("gpt"):
                response = await self.get_openai_response(prompt)
            elif self.anthropic_api_key and model == "claude":
                response = await self.get_claude_response(prompt)
            elif self.google_api_key and model == "gemini":
                response = await self.get_gemini_response(prompt)
            else:
                response = "No AI service is currently available."

            return response

        except Exception as e:
            return f"An error occurred: {str(e)}"

    async def get_openai_response(self, prompt: str) -> str:
        """Get response from OpenAI's GPT"""
        try:
            response = await asyncio.to_thread(
                openai.ChatCompletion.create,
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"OpenAI Error: {str(e)}"

    async def get_claude_response(self, prompt: str) -> str:
        """Get response from Anthropic's Claude"""
        try:
            response = await asyncio.to_thread(
                self.claude.messages.create,
                model="claude-3-sonnet-20240229",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            return f"Claude Error: {str(e)}"

    async def get_gemini_response(self, prompt: str) -> str:
        """Get response from Google's Gemini"""
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = await asyncio.to_thread(
                model.generate_content,
                prompt
            )
            return response.text
        except Exception as e:
            return f"Gemini Error: {str(e)}"

    async def check_cooldown(self, user_id: str) -> bool:
        """Check if user is on cooldown"""
        if user_id in self.cooldowns:
            if datetime.now() < self.cooldowns[user_id]:
                return False
        self.cooldowns[user_id] = datetime.now() + timedelta(minutes=self.COOLDOWN_MINUTES)
        return True

    @app_commands.command(name="ask", description="Ask a question to the AI assistant")
    async def ask(self, interaction: discord.Interaction, question: str, model: Optional[str] = "gpt-3.5-turbo"):
        """Ask a general question to the AI assistant"""
        await interaction.response.defer()
        answer = await self.get_ai_response(question, str(interaction.user.id), model)
        
        embed = discord.Embed(
            title="AI Assistant Response",
            description=answer,
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        embed.set_footer(text=f"Requested by {interaction.user.name} | Model: {model}")
        
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="codehelp", description="Get coding help")
    async def codehelp(self, interaction: discord.Interaction, code: str, language: Optional[str] = None):
        """Get coding help from the AI assistant"""
        await interaction.response.defer()
        
        prompt = f"Please help with this code in {language if language else 'any language'}:\n```\n{code}\n```"
        response = await self.get_ai_response(prompt, str(interaction.user.id))
        
        embed = discord.Embed(
            title="Code Help",
            description=response,
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        embed.set_footer(text=f"Requested by {interaction.user.name}")
        
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="explain", description="Explain code in simple terms")
    async def explain(self, interaction: discord.Interaction, code: str):
        """Explain code in simple terms"""
        await interaction.response.defer()
        
        prompt = f"Explain this code in simple terms:\n```\n{code}\n```"
        explanation = await self.get_ai_response(prompt, str(interaction.user.id))
        
        embed = discord.Embed(
            title="Code Explanation",
            description=explanation,
            color=discord.Color.purple(),
            timestamp=datetime.now()
        )
        embed.set_footer(text=f"Requested by {interaction.user.name}")
        
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AIAssistant(bot))