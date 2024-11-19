import discord
from discord.ext import commands
from discord import app_commands
from transformers import AutoTokenizer, AutoModelForCausalLM
import os

class CodingHelp(commands.Cog):
    """Cog for providing coding help using AI"""

    def __init__(self, bot):
        self.bot = bot
        self.tokenizer = AutoTokenizer.from_pretrained("nvidia/Llama-3.1-Nemotron-70B-Instruct-HF")
        self.model = AutoModelForCausalLM.from_pretrained("nvidia/Llama-3.1-Nemotron-70B-Instruct-HF")

    async def is_premium(self, user_id):
        # Placeholder for checking if the user has a premium subscription
        return True

    async def generate_response(self, prompt):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(inputs.input_ids, max_length=150)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response

    @commands.command(name="explain")
    async def explain_command(self, ctx, *, code: str):
        """Explain code in simple terms"""
        if not await self.is_premium(ctx.author.id):
            await ctx.send("This is a premium feature. Please subscribe to access it.")
            return

        try:
            prompt = f"Explain the following code in simple terms:\n{code}"
            answer = await self.generate_response(prompt)
            await ctx.send(answer)
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

    @commands.command(name="debug")
    async def debug_command(self, ctx, *, code: str):
        """Help debug code issues"""
        if not await self.is_premium(ctx.author.id):
            await ctx.send("This is a premium feature. Please subscribe to access it.")
            return

        try:
            prompt = f"Debug the following code:\n{code}"
            answer = await self.generate_response(prompt)
            await ctx.send(answer)
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

    @commands.command(name="optimize")
    async def optimize_command(self, ctx, *, code: str):
        """Suggest code optimizations"""
        if not await self.is_premium(ctx.author.id):
            await ctx.send("This is a premium feature. Please subscribe to access it.")
            return

        try:
            prompt = f"Optimize the following code:\n{code}"
            answer = await self.generate_response(prompt)
            await ctx.send(answer)
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

    @app_commands.command(name="explain", description="Explain code in simple terms")
    async def explain(self, interaction: discord.Interaction, code: str):
        """Explain code in simple terms"""
        if not await self.is_premium(interaction.user.id):
            await interaction.response.send_message("This is a premium feature. Please subscribe to access it.", ephemeral=True)
            return

        try:
            prompt = f"Explain the following code in simple terms:\n{code}"
            answer = await self.generate_response(prompt)
            await interaction.response.send_message(answer)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @app_commands.command(name="debug", description="Help debug code issues")
    async def debug(self, interaction: discord.Interaction, code: str):
        """Help debug code issues"""
        if not await self.is_premium(interaction.user.id):
            await interaction.response.send_message("This is a premium feature. Please subscribe to access it.", ephemeral=True)
            return

        try:
            prompt = f"Debug the following code:\n{code}"
            answer = await self.generate_response(prompt)
            await interaction.response.send_message(answer)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @app_commands.command(name="optimize", description="Suggest code optimizations")
    async def optimize(self, interaction: discord.Interaction, code: str):
        """Suggest code optimizations"""
        if not await self.is_premium(interaction.user.id):
            await interaction.response.send_message("This is a premium feature. Please subscribe to access it.", ephemeral=True)
            return

        try:
            prompt = f"Optimize the following code:\n{code}"
            answer = await self.generate_response(prompt)
            await interaction.response.send_message(answer)
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

async def setup(bot):
    await bot.add_cog(CodingHelp(bot))