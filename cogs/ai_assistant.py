from datetime import datetime, timedelta
import logging
import aiohttp
import discord
from discord.ext import commands
from discord import app_commands
import anthropic
import google.generativeai as genai
import os
from typing import Optional, Dict, Any
import asyncio
import json

logger = logging.getLogger(__name__)

class AIAssistant(commands.Cog):
    """AI-powered assistance for developers"""
    
    def __init__(self, bot):
        self.bot = bot
        self.api_url = "http://localhost:8000"  # URL of the model server
        self.session = aiohttp.ClientSession()
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

    def cog_unload(self):
        """Cleanup when cog is unloaded"""
        if self.session:
            self.bot.loop.create_task(self.session.close())
    
    async def _call_model_api(
        self,
        endpoint: str,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Make request to model API"""
        try:
            async with self.session.post(
                f"{self.api_url}/{endpoint}",
                json=payload
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(
                        f"API error: {response.status} - {error_text}"
                    )
                    return {"error": f"API error: {response.status}"}
                return await response.json()
        except Exception as e:
            logger.error(f"API request failed: {str(e)}")
            return {"error": f"API request failed: {str(e)}"}
    
    @commands.command()
    async def ask(self, ctx, *, question: str):
        """Ask the AI assistant a question"""
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

    @commands.command()
    async def review(self, ctx, *, code: str):
        """Review code for improvements"""
        # Strip code blocks if present
        if code.startswith("```") and code.endswith("```"):
            code = code[3:-3]
            # Remove language identifier if present
            if "\n" in code:
                code = code[code.index("\n")+1:]
        
        async with ctx.typing():
            response = await self._call_model_api(
                "analyze",
                {
                    "code": code,
                    "analysis_type": "all",
                    "max_length": 1024,
                }
            )
            
            if "error" in response:
                await ctx.send(f"Sorry, I encountered an error: {response['error']}")
                return
            
            results = response["analysis_results"]
            
            # Create detailed embed
            embed = discord.Embed(
                title="Code Review Results",
                description=results["summary"],
                color=discord.Color.blue()
            )
            
            if results.get("security_issues"):
                issues = "\n".join(f"• {issue}" for issue in results["security_issues"])
                embed.add_field(
                    name="🔒 Security Issues",
                    value=issues or "No security issues found",
                    inline=False
                )
            
            if results.get("performance_tips"):
                tips = "\n".join(f"• {tip}" for tip in results["performance_tips"])
                embed.add_field(
                    name="⚡ Performance Tips",
                    value=tips or "No performance issues found",
                    inline=False
                )
            
            if results.get("style_suggestions"):
                suggestions = "\n".join(
                    f"• {suggestion}" for suggestion in results["style_suggestions"]
                )
                embed.add_field(
                    name="✨ Style Suggestions",
                    value=suggestions or "No style issues found",
                    inline=False
                )
            
            await ctx.send(embed=embed)
    
    @commands.command()
    async def optimize(self, ctx, *, code: str):
        """Suggest optimizations for code"""
        # Strip code blocks if present
        if code.startswith("```") and code.endswith("```"):
            code = code[3:-3]
            # Remove language identifier if present
            if "\n" in code:
                code = code[code.index("\n")+1:]
        
        async with ctx.typing():
            response = await self._call_model_api(
                "analyze",
                {
                    "code": code,
                    "analysis_type": "performance",
                    "max_length": 1024,
                }
            )
            
            if "error" in response:
                await ctx.send(f"Sorry, I encountered an error: {response['error']}")
                return
            
            results = response["analysis_results"]
            
            embed = discord.Embed(
                title="Code Optimization Suggestions",
                description=results["summary"],
                color=discord.Color.green()
            )
            
            details = "\n".join(f"• {detail}" for detail in results["details"])
            if details:
                embed.add_field(
                    name="Optimization Details",
                    value=details,
                    inline=False
                )
            
            await ctx.send(embed=embed)
    
    @commands.command()
    async def explain(self, ctx, *, code: str):
        """Explain what code does"""
        # Strip code blocks if present
        if code.startswith("```") and code.endswith("```"):
            code = code[3:-3]
            # Remove language identifier if present
            if "\n" in code:
                code = code[code.index("\n")+1:]
        
        async with ctx.typing():
            response = await self._call_model_api(
                "generate",
                {
                    "prompt": f"Explain this code:\n\n{code}\n\nExplanation:",
                    "max_length": 1024,
                    "temperature": 0.7,
                    "top_p": 0.9,
                }
            )
            
            if "error" in response:
                await ctx.send(f"Sorry, I encountered an error: {response['error']}")
                return
            
            explanation = response["generated_text"]
            
            # Split into chunks if needed
            chunks = [explanation[i:i+1900] for i in range(0, len(explanation), 1900)]
            
            for i, chunk in enumerate(chunks):
                embed = discord.Embed(
                    title="Code Explanation" if i == 0 else "Code Explanation (continued)",
                    description=chunk,
                    color=discord.Color.blue()
                )
                await ctx.send(embed=embed)
    
    @commands.command()
    async def improve(self, ctx, *, code: str):
        """Suggest improvements for code"""
        # Strip code blocks if present
        if code.startswith("```") and code.endswith("```"):
            code = code[3:-3]
            # Remove language identifier if present
            if "\n" in code:
                code = code[code.index("\n")+1:]
        
        async with ctx.typing():
            response = await self._call_model_api(
                "analyze",
                {
                    "code": code,
                    "analysis_type": "style",
                    "max_length": 1024,
                }
            )
            
            if "error" in response:
                await ctx.send(f"Sorry, I encountered an error: {response['error']}")
                return
            
            results = response["analysis_results"]
            
            embed = discord.Embed(
                title="Code Improvement Suggestions",
                description=results["summary"],
                color=discord.Color.gold()
            )
            
            details = "\n".join(f"• {detail}" for detail in results["details"])
            if details:
                embed.add_field(
                    name="Improvement Details",
                    value=details,
                    inline=False
                )
            
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AIAssistant(bot))