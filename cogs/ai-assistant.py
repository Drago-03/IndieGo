import discord
from discord.ext import commands
import openai
import anthropic
import google.generativeai as genai
import os
import random

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
            return f"OpenAI Error: {str(e)}"

    async def get_claude_response(self, prompt, system_prompt):
        try:
            message = await self.claude.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1024,
                system=system_prompt,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content
        except Exception as e:
            return f"Claude Error: {str(e)}"

    async def get_gemini_response(self, prompt):
        try:
            response = await self.gemini.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Gemini Error: {str(e)}"

    @commands.command()
    async def codehelp(self, ctx, *, question):
        """Get coding help using multiple AI models"""
        system_prompt = """You are an expert programming assistant. Provide clear, 
        concise explanations with practical code examples. Focus on best practices 
        and modern development approaches."""
        
        # Randomly select an AI provider
        provider = random.choice(['openai', 'claude', 'gemini'])
        
        async with ctx.typing():
            if provider == 'openai':
                answer = await self.get_openai_response(question, system_prompt)
            elif provider == 'claude':
                answer = await self.get_claude_response(question, system_prompt)
            else:
                answer = await self.get_gemini_response(question)

            # Split long responses
            if len(answer) > 2000:
                parts = [answer[i:i+1990] for i in range(0, len(answer), 1990)]
                for part in parts:
                    await ctx.send(f"```{part}```")
            else:
                await ctx.send(f"```{answer}```")

    @commands.command()
    async def ask(self, ctx, *, question):
        """Ask a general question to the AI assistant"""
        system_prompt = """You are a helpful assistant in a developer community. 
        Provide friendly, informative responses while maintaining professionalism."""
        
        # Randomly select an AI provider
        provider = random.choice(['openai', 'claude', 'gemini'])
        
        async with ctx.typing():
            if provider == 'openai':
                answer = await self.get_openai_response(question, system_prompt)
            elif provider == 'claude':
                answer = await self.get_claude_response(question, system_prompt)
            else:
                answer = await self.get_gemini_response(question)

            # Split long responses
            if len(answer) > 2000:
                parts = [answer[i:i+1990] for i in range(0, len(answer), 1990)]
                for part in parts:
                    await ctx.send(part)
            else:
                await ctx.send(answer)

async def setup(bot):
    await bot.add_cog(AIAssistant(bot))