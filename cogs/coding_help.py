import discord
from discord.ext import commands
from discord import app_commands
import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

class CodingHelp(commands.Cog):
    """Cog for providing coding help using AI"""

    def __init__(self, bot):
        self.bot = bot

    async def is_premium(self, user_id):
        # Check if the user has a premium subscription
        try:
            with open('premium_users.json', 'r') as f:
                premium_users = json.load(f)
            if user_id in premium_users:
                return True
        except FileNotFoundError:
            return False
        return False

    @app_commands.command(name="code", description="Get coding help")
    async def code(self, interaction: discord.Interaction, question: str):
        """Get coding help"""
        if not await self.is_premium(interaction.user.id):
            await interaction.response.send_message("This is a premium feature. Please subscribe to access it.", ephemeral=True)
            return

        try:
            response = await openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful coding assistant. Provide clear, concise code examples and explanations."},
                    {"role": "user", "content": question}
                ]
            )
            
            answer = response.choices[0].message.content
            
            if len(answer) > 1900:
                # Split long responses into multiple messages
                chunks = [answer[i:i+1900] for i in range(0, len(answer), 1900)]
                for chunk in chunks:
                    await interaction.response.send_message(f"```{chunk}```")
            else:
                await interaction.response.send_message(f"```{answer}```")
                
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @app_commands.command(name="explain", description="Explain code in simple terms")
    async def explain(self, interaction: discord.Interaction, code: str):
        """Explain code in simple terms"""
        if not await self.is_premium(interaction.user.id):
            await interaction.response.send_message("This is a premium feature. Please subscribe to access it.", ephemeral=True)
            return

        try:
            response = await openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful coding assistant. Explain the provided code in simple terms."},
                    {"role": "user", "content": f"Explain this code: {code}"}
                ]
            )
            
            await interaction.response.send_message(response.choices[0].message.content)
            
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @app_commands.command(name="debug", description="Help debug code issues")
    async def debug(self, interaction: discord.Interaction, code: str):
        """Help debug code issues"""
        if not await self.is_premium(interaction.user.id):
            await interaction.response.send_message("This is a premium feature. Please subscribe to access it.", ephemeral=True)
            return

        try:
            response = await openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful coding assistant. Help debug the provided code."},
                    {"role": "user", "content": f"Debug this code: {code}"}
                ]
            )
            
            await interaction.response.send_message(response.choices[0].message.content)
            
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @app_commands.command(name="optimize", description="Suggest code optimizations")
    async def optimize(self, interaction: discord.Interaction, code: str):
        """Suggest code optimizations"""
        if not await self.is_premium(interaction.user.id):
            await interaction.response.send_message("This is a premium feature. Please subscribe to access it.", ephemeral=True)
            return

        try:
            response = await openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful coding assistant. Suggest optimizations for the provided code."},
                    {"role": "user", "content": f"Optimize this code: {code}"}
                ]
            )
            
            await interaction.response.send_message(response.choices[0].message.content)
            
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

    @app_commands.command(name="scan_image", description="Scan an image for code and provide help")
    async def scan_image(self, interaction: discord.Interaction, image_url: str):
        """Scan an image for code and provide help"""
        if not await self.is_premium(interaction.user.id):
            await interaction.response.send_message("This is a premium feature. Please subscribe to access it.", ephemeral=True)
            return

        try:
            # Placeholder for image scanning logic
            # You can use OCR libraries like pytesseract to extract text from images
            extracted_code = "def example():\n    return True"  # Example extracted code
            
            response = await openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful coding assistant. Provide help for the extracted code."},
                    {"role": "user", "content": f"Help with this code: {extracted_code}"}
                ]
            )
            
            await interaction.response.send_message(response.choices[0].message.content)
            
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

async def setup(bot):
    await bot.add_cog(CodingHelp(bot))