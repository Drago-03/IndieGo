import discord
from discord.ext import commands
import openai
import anthropic
import google.generativeai as genai
import os
import random
from discord import app_commands
import asyncio
from dotenv import load_dotenv
import json

from config import INSTALL_URL

load_dotenv()

# Bot Configuration
TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PREFIX = '.'
TICKET_CATEGORY_ID = None
STAFF_ROLE_ID = None
LOG_CHANNEL_ID = 1308525133048188949

# URLs and Endpoints
BOT_WEBSITE = "https://drago-03.github.io/IndieGo-Website/"
INTERACTIONS_URL = f"{BOT_WEBSITE}/api/interactions"
LINKED_ROLES_URL = f"{BOT_WEBSITE}/api/linked-roles"
TERMS_URL = f"{BOT_WEBSITE}/terms"
PRIVACY_URL = f"{BOT_WEBSITE}/privacy"
INSTALL_URL = f"https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=8&scope=bot%20applications.commands"
OAUTH2_URL = f"https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&redirect_uri={BOT_WEBSITE}/callback&response_type=code&scope=identify%20guilds"

# Branding
EMBED_COLOR = 0x9F7AEA  # Purple

class AIAssistant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Initialize AI clients
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.claude = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.gemini = genai.GenerativeModel('gemini-pro')

    async def get_openai_response(self, prompt, system_prompt):
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"An error occurred: {str(e)}"

    @commands.command(name="ask")
    async def ask_command(self, ctx, *, question: str):
        """Ask a general question to the AI assistant"""
        answer = await self.get_openai_response(question, "You are a helpful assistant.")
        await ctx.send(answer)

    @app_commands.command(name="ask", description="Ask a general question to the AI assistant")
    async def ask(self, interaction: discord.Interaction, question: str):
        """Ask a general question to the AI assistant"""
        answer = await self.get_openai_response(question, "You are a helpful assistant.")
        await interaction.response.send_message(answer)

    @commands.command(name="codehelp")
    async def codehelp_command(self, ctx, *, code: str):
        """Get coding help using multiple AI models"""
        help_response = await self.get_openai_response(code, "You are a helpful coding assistant.")
        await ctx.send(help_response)

    @app_commands.command(name="codehelp", description="Get coding help using multiple AI models")
    async def codehelp(self, interaction: discord.Interaction, code: str):
        """Get coding help using multiple AI models"""
        help_response = await self.get_openai_response(code, "You are a helpful coding assistant.")
        await interaction.response.send_message(help_response)

async def setup(bot):
    await bot.add_cog(AIAssistant(bot))