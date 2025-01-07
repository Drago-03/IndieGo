import discord
from discord.ext import commands
import anthropic
import google.generativeai as genai
import os
from typing import Optional
import asyncio
import aiohttp

class InteractiveDM(commands.Cog):
    """Cog for handling interactive DM interactions"""

    def __init__(self, bot):
        self.bot = bot
        self.anthropic_client = anthropic.Client(api_key=os.getenv('ANTHROPIC_API_KEY'))
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-pro')
        self.conversation_context = {}

    async def fetch_claude_response(self, prompt: str) -> str:
        """Get response from Claude"""
        try:
            message = await self.anthropic_client.messages.create(
                model="claude-2",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            return f"Sorry, I'm having trouble thinking right now: {str(e)}"

    async def fetch_gemini_response(self, prompt: str) -> str:
        """Get response from Gemini"""
        try:
            response = await self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Hmm, I need a moment to think: {str(e)}"

    async def select_best_response(self, claude_response: str, gemini_response: str) -> str:
        """Select the better response"""
        if len(claude_response) > len(gemini_response) * 1.2:
            return claude_response
        elif len(gemini_response) > len(claude_response) * 1.2:
            return gemini_response
        return claude_response

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        should_respond = False
        if self.bot.user in message.mentions:
            should_respond = True
        elif message.reference:
            referenced_msg = await message.channel.fetch_message(message.reference.message_id)
            if referenced_msg.author.id == self.bot.user.id:
                should_respond = True

        if should_respond:
            channel_id = str(message.channel.id)
            
            # Get conversation context
            if channel_id not in self.conversation_context:
                self.conversation_context[channel_id] = []
            
            # Add message to context
            self.conversation_context[channel_id].append(f"{message.author.name}: {message.content}")
            
            # Keep only last 5 messages for context
            self.conversation_context[channel_id] = self.conversation_context[channel_id][-5:]
            
            async with message.channel.typing():
                try:
                    # Create prompt with context
                    context = "\n".join(self.conversation_context[channel_id])
                    prompt = (
                        "You are having a casual conversation. Be helpful but natural in your response. "
                        f"Previous messages:\n{context}\n\n"
                        "Reply in a conversational way without any special formatting or labels."
                    )

                    # Get and select best response
                    tasks = [
                        self.fetch_claude_response(prompt),
                        self.fetch_gemini_response(prompt)
                    ]
                    claude_response, gemini_response = await asyncio.gather(*tasks)
                    response = await self.select_best_response(claude_response, gemini_response)
                    
                    # Clean up response
                    response = response.replace("AI:", "").replace("Assistant:", "").replace("Bot:", "").strip()
                    
                    # Send response and update context
                    await message.reply(response)
                    self.conversation_context[channel_id].append(f"Bot: {response}")

                except Exception as e:
                    await message.reply("Sorry, I'm having trouble responding right now!")

async def setup(bot):
    await bot.add_cog(InteractiveDM(bot))