import discord
from discord.ext import commands
from discord import app_commands
import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging
from typing import Dict, Set, List, Optional, Any
import aiohttp
import json
import asyncio
import random
import time

# Load environment variables
load_dotenv()
logger = logging.getLogger('IndieGOBot')

class Chat(commands.Cog):
    """Cog for natural conversations with students"""
    
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        self.enabled_channels: Set[int] = set()
        self.conversation_context: Dict[int, list] = {}
        self.service_cooldowns: Dict[str, float] = {}
        
        # Initialize Gemini if API key is available
        self.gemini_model = None
        try:
            api_key = os.getenv('GOOGLE_API_KEY')
            if api_key:
                genai.configure(api_key=api_key)
                self.gemini_model = genai.GenerativeModel('gemini-pro')
                logger.info("Successfully initialized Gemini AI model")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini: {str(e)}")
        
        # Personality traits for the bot
        self.personality = """You are IndieGO, a friendly and supportive AI assistant in a Discord server for students interested in development and design. Your traits:
- Enthusiastic about helping students learn and grow
- Knowledgeable about programming, web development, and design
- Patient and encouraging, especially with beginners
- Uses casual, friendly language while remaining professional
- Shares relevant examples and resources
- Asks thoughtful follow-up questions to better understand students' needs
- Celebrates students' successes and provides constructive feedback
- Has a sense of humor but keeps interactions appropriate
- Encourages collaboration and learning from peers
- Provides explanations at the right level for each student"""

    async def cog_unload(self):
        if self.session:
            await self.session.close()

    def _is_on_cooldown(self, service: str, cooldown_seconds: int = 60) -> bool:
        """Check if a service is on cooldown"""
        current_time = time.time()
        last_failure = self.service_cooldowns.get(service, 0)
        return current_time - last_failure < cooldown_seconds

    def _set_cooldown(self, service: str):
        """Set a service on cooldown after failure"""
        self.service_cooldowns[service] = time.time()

    async def get_gemini_response(self, prompt: str) -> Optional[str]:
        """Get response from Gemini AI"""
        if not self.gemini_model or self._is_on_cooldown("gemini"):
            return None
            
        try:
            response = await asyncio.wait_for(
                asyncio.to_thread(self.gemini_model.generate_content, prompt),
                timeout=10.0
            )
            return response.text
        except Exception as e:
            logger.error(f"Gemini error: {str(e)}")
            self._set_cooldown("gemini")
            return None

    async def get_huggingface_response(self, prompt: str) -> Optional[str]:
        """Get response from HuggingFace API"""
        if self._is_on_cooldown("huggingface"):
            return None
            
        try:
            # Try different models if one fails
            models = [
                "HuggingFaceH4/zephyr-7b-beta",
                "mistralai/Mistral-7B-Instruct-v0.2",
                "facebook/opt-1.3b",
                "microsoft/DialoGPT-medium"
            ]
            
            for model in models:
                if self._is_on_cooldown(f"huggingface_{model}"):
                    continue
                    
                url = f"https://api-inference.huggingface.co/models/{model}"
                headers = {"Content-Type": "application/json"}
                
                payload = {
                    "inputs": prompt,
                    "parameters": {
                        "max_new_tokens": 250,
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "do_sample": True
                    }
                }
                
                try:
                    async with self.session.post(url, headers=headers, json=payload, timeout=10) as response:
                        if response.status == 200:
                            result = await response.json()
                            if isinstance(result, list) and len(result) > 0:
                                text = result[0].get("generated_text", "")
                                # Remove the prompt from the response
                                if text.startswith(prompt):
                                    text = text[len(prompt):].strip()
                                return text
                        else:
                            self._set_cooldown(f"huggingface_{model}")
                except Exception as e:
                    logger.error(f"Error with model {model}: {str(e)}")
                    self._set_cooldown(f"huggingface_{model}")
                    continue  # Try next model
                    
            self._set_cooldown("huggingface")
            return None
        except Exception as e:
            logger.error(f"HuggingFace error: {str(e)}")
            self._set_cooldown("huggingface")
            return None

    async def get_you_api_response(self, prompt: str) -> Optional[str]:
        """Get response from You.com API"""
        if self._is_on_cooldown("you_api"):
            return None
            
        try:
            url = "https://you.com/api/streamingSearch"
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            
            data = {
                "q": prompt,
                "page": 1,
                "count": 10,
                "safeSearch": "Moderate",
                "onShoppingPage": False,
                "responseFilter": "WebPages",
                "domain": "youchat"
            }
            
            async with self.session.post(url, headers=headers, json=data, timeout=10) as response:
                if response.status == 200:
                    result = await response.text()
                    # Parse the response and extract the answer
                    try:
                        messages = result.strip().split('\n')
                        for message in messages:
                            if message:
                                data = json.loads(message)
                                if 'youChatToken' in data:
                                    return data['youChatToken']
                    except Exception as e:
                        logger.error(f"Error parsing You.com response: {str(e)}")
                        return None
                else:
                    self._set_cooldown("you_api")
                    return None
                    
        except Exception as e:
            logger.error(f"You.com API error: {str(e)}")
            self._set_cooldown("you_api")
            return None

    async def get_perplexity_response(self, prompt: str) -> Optional[str]:
        """Get response from Perplexity API"""
        if self._is_on_cooldown("perplexity"):
            return None
            
        try:
            url = "https://labs-api.perplexity.ai/chat/completions"
            headers = {
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "llama-3-sonar-small-32k-online",
                "messages": [
                    {"role": "system", "content": self.personality},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 250
            }
            
            async with self.session.post(url, headers=headers, json=data, timeout=10) as response:
                if response.status == 200:
                    result = await response.json()
                    if "choices" in result and len(result["choices"]) > 0:
                        return result["choices"][0]["message"]["content"]
                else:
                    self._set_cooldown("perplexity")
                    return None
                    
        except Exception as e:
            logger.error(f"Perplexity API error: {str(e)}")
            self._set_cooldown("perplexity")
            return None

    async def get_ollama_response(self, prompt: str) -> Optional[str]:
        """Get response from Ollama API if running locally"""
        if self._is_on_cooldown("ollama"):
            return None
            
        try:
            # Assuming Ollama is running locally on default port
            url = "http://localhost:11434/api/generate"
            headers = {"Content-Type": "application/json"}
            
            data = {
                "model": "llama3",  # or any other model you have pulled
                "prompt": prompt,
                "stream": False
            }
            
            async with self.session.post(url, headers=headers, json=data, timeout=15) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get("response", "")
                else:
                    self._set_cooldown("ollama")
                    return None
                    
        except Exception as e:
            # This is expected to fail if Ollama is not running locally
            self._set_cooldown("ollama")
            return None

    async def get_fallback_response(self, prompt: str) -> str:
        """Simple rule-based fallback when all APIs fail"""
        # Extract the user's message from the prompt
        user_message = ""
        if "User:" in prompt:
            user_message = prompt.split("User:")[-1].split("\n")[0].strip()
        
        # Simple responses based on keywords
        greetings = ["hi", "hello", "hey", "greetings", "howdy"]
        if any(greeting in user_message.lower() for greeting in greetings):
            return random.choice([
                "Hello there! How can I help you today?",
                "Hi! What can I assist you with?",
                "Hey! I'm here to help. What's up?",
                "Greetings! How can I be of service today?"
            ])
            
        questions = ["how", "what", "why", "when", "where", "who", "can", "could", "would", "?"]
        if any(q in user_message.lower() for q in questions):
            return random.choice([
                "That's a great question! I'd love to help, but I'm having some technical difficulties right now. Could you try asking again in a moment?",
                "I'm thinking about your question, but my systems are a bit slow right now. Could you try rephrasing or asking again later?",
                "I want to give you a good answer, but I'm experiencing some technical issues. Let me get back to you on that soon!",
                "Interesting question! I'm currently processing a lot of requests. Could you try again in a bit?"
            ])
            
        # Default responses
        return random.choice([
            "I'm here and listening! Could you tell me more about that?",
            "That's interesting! Could you elaborate a bit more?",
            "I'd love to continue this conversation, but I'm having some technical difficulties. Let's chat more in a moment!",
            "I appreciate your message! I'm currently processing a lot of information. What else would you like to discuss?",
            "Thanks for reaching out! I'm here to help with any questions about programming or design."
        ])

    async def get_ai_response(self, prompt: str) -> str:
        """Get response with fallback mechanisms"""
        # Try all services in parallel for faster response
        tasks = [
            self.get_gemini_response(prompt),
            self.get_huggingface_response(prompt),
            self.get_you_api_response(prompt),
            self.get_perplexity_response(prompt),
            self.get_ollama_response(prompt)
        ]
        
        # Wait for first successful response or all to fail
        for future in asyncio.as_completed(tasks, timeout=15):
            try:
                result = await future
                if result:
                    return result
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error in get_ai_response: {str(e)}")
                continue
        
        # If all services failed, use the rule-based fallback
        return await self.get_fallback_response(prompt)

    @commands.hybrid_command(
        name="enable_chat",
        description="Enable natural chat interactions in a channel"
    )
    @commands.has_permissions(manage_channels=True)
    @app_commands.describe(channel="The channel to enable chat in")
    async def enable_chat(self, ctx, channel: discord.TextChannel = None):
        """Enable natural chat interactions in a channel"""
        channel = channel or ctx.channel
        if channel.id in self.enabled_channels:
            await ctx.send(f"Chat is already enabled in {channel.mention}!")
            return
            
        self.enabled_channels.add(channel.id)
        self.conversation_context[channel.id] = []
        await ctx.send(f"✅ Chat enabled in {channel.mention}! I'll respond to messages when mentioned or replied to.")
        logger.info(f"Chat enabled in channel {channel.id} by {ctx.author}")

    @commands.hybrid_command(
        name="disable_chat",
        description="Disable natural chat interactions in a channel"
    )
    @commands.has_permissions(manage_channels=True)
    @app_commands.describe(channel="The channel to disable chat in")
    async def disable_chat(self, ctx, channel: discord.TextChannel = None):
        """Disable natural chat interactions in a channel"""
        channel = channel or ctx.channel
        if channel.id not in self.enabled_channels:
            await ctx.send(f"Chat is not enabled in {channel.mention}!")
            return
            
        self.enabled_channels.remove(channel.id)
        if channel.id in self.conversation_context:
            del self.conversation_context[channel.id]
        await ctx.send(f"❌ Chat disabled in {channel.mention}.")
        logger.info(f"Chat disabled in channel {channel.id} by {ctx.author}")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Handle natural conversations in enabled channels"""
        # Ignore bot messages
        if message.author.bot:
            return
            
        # Check if this is an enabled channel
        if message.channel.id not in self.enabled_channels:
            return
            
        should_respond = False
        # Check if bot was mentioned
        if self.bot.user in message.mentions:
            should_respond = True
        # Check if message is a reply to bot
        elif message.reference:
            try:
                referenced_msg = await message.channel.fetch_message(message.reference.message_id)
                if referenced_msg.author.id == self.bot.user.id:
                    should_respond = True
            except discord.NotFound:
                pass
        # Check if bot's name was mentioned
        elif "indiego" in message.content.lower():
            should_respond = True
            
        if should_respond:
            async with message.channel.typing():
                # Get conversation context
                context = self.conversation_context.get(message.channel.id, [])[-3:]  # Last 3 messages for performance
                context_str = "\n".join(context)
                
                # Create prompt with personality and context
                prompt = f"{self.personality}\n\nPrevious conversation:\n{context_str}\n\nUser: {message.content}\n\nRespond naturally:"
                
                # Get response with fallback mechanisms
                response = await self.get_ai_response(prompt)
                
                # Clean up response
                response = response.replace("AI:", "").replace("Assistant:", "").replace("IndieGO:", "").strip()
                
                # Update context
                self.conversation_context.setdefault(message.channel.id, []).append(f"{message.author.name}: {message.content}")
                self.conversation_context[message.channel.id].append(f"IndieGO: {response}")
                
                # Send response with retry mechanism
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        await message.reply(response)
                        break
                    except discord.HTTPException as e:
                        logger.error(f"Failed to send message (attempt {attempt+1}/{max_retries}): {str(e)}")
                        if attempt == max_retries - 1:  # Last attempt, try channel send
                            try:
                                await message.channel.send(f"{message.author.mention} {response}")
                            except discord.HTTPException:
                                logger.error("Failed to send fallback message")
                        else:
                            # Wait before retrying
                            await asyncio.sleep(1)

    @commands.hybrid_command(
        name="reset_chat",
        description="Reset the conversation context in a channel"
    )
    @commands.has_permissions(manage_channels=True)
    @app_commands.describe(channel="The channel to reset chat context in")
    async def reset_chat(self, ctx, channel: discord.TextChannel = None):
        """Reset the conversation context in a channel"""
        channel = channel or ctx.channel
        if channel.id not in self.enabled_channels:
            await ctx.send(f"Chat is not enabled in {channel.mention}!")
            return
            
        if channel.id in self.conversation_context:
            self.conversation_context[channel.id] = []
        await ctx.send(f"🔄 Chat context has been reset in {channel.mention}.")
        logger.info(f"Chat context reset in channel {channel.id} by {ctx.author}")

async def setup(bot):
    await bot.add_cog(Chat(bot)) 