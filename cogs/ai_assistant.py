import discord
from discord.ext import commands
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
TOKEN = os.getenv('DISCORD_TOKEN')
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
        self.tokenizer = AutoTokenizer.from_pretrained("nvidia/Llama-3.1-Nemotron-70B-Instruct-HF")
        self.model = AutoModelForCausalLM.from_pretrained("nvidia/Llama-3.1-Nemotron-70B-Instruct-HF")

    async def generate_response(self, prompt):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(inputs.input_ids, max_length=150)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response

    @commands.command(name="ask")
    async def ask_command(self, ctx, *, question: str):
        """Ask a general question to the AI assistant"""
        answer = await self.generate_response(question)
        await ctx.send(answer)

    @app_commands.command(name="ask", description="Ask a general question to the AI assistant")
    async def ask(self, interaction: discord.Interaction, question: str):
        """Ask a general question to the AI assistant"""
        answer = await self.generate_response(question)
        await interaction.response.send_message(answer)

    @commands.command(name="codehelp")
    async def codehelp_command(self, ctx, *, code: str):
        """Get coding help using the AI assistant"""
        help_response = await self.generate_response(code)
        await ctx.send(help_response)

    @app_commands.command(name="codehelp", description="Get coding help using the AI assistant")
    async def codehelp(self, interaction: discord.Interaction, code: str):
        """Get coding help using the AI assistant"""
        help_response = await self.generate_response(code)
        await interaction.response.send_message(help_response)

    @commands.command(name="explain")
    async def explain_command(self, ctx, *, code: str):
        """Explain code in simple terms"""
        explanation = await self.generate_response(f"Explain the following code in simple terms:\n{code}")
        await ctx.send(explanation)

    @app_commands.command(name="explain", description="Explain code in simple terms")
    async def explain(self, interaction: discord.Interaction, code: str):
        """Explain code in simple terms"""
        explanation = await self.generate_response(f"Explain the following code in simple terms:\n{code}")
        await interaction.response.send_message(explanation)

    @commands.command(name="debug")
    async def debug_command(self, ctx, *, code: str):
        """Help debug code issues"""
        debug_response = await self.generate_response(f"Debug the following code:\n{code}")
        await ctx.send(debug_response)

    @app_commands.command(name="debug", description="Help debug code issues")
    async def debug(self, interaction: discord.Interaction, code: str):
        """Help debug code issues"""
        debug_response = await self.generate_response(f"Debug the following code:\n{code}")
        await interaction.response.send_message(debug_response)

    @commands.command(name="optimize")
    async def optimize_command(self, ctx, *, code: str):
        """Suggest code optimizations"""
        optimization = await self.generate_response(f"Optimize the following code:\n{code}")
        await ctx.send(optimization)

    @app_commands.command(name="optimize", description="Suggest code optimizations")
    async def optimize(self, interaction: discord.Interaction, code: str):
        """Suggest code optimizations"""
        optimization = await self.generate_response(f"Optimize the following code:\n{code}")
        await interaction.response.send_message(optimization)

async def setup(bot):
    await bot.add_cog(AIAssistant(bot))