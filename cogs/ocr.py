import discord
from discord.ext import commands
from PIL import Image
import pytesseract
import io

class OCR(commands.Cog):
    """Cog for OCR and image scanning"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="scan")
    async def scan_command(self, ctx):
        """Scan an image for text"""
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]
            image_data = await attachment.read()
            image = Image.open(io.BytesIO(image_data))
            text = pytesseract.image_to_string(image)
            await ctx.send(f"Extracted text:\n{text}")
        else:
            await ctx.send("Please attach an image to scan.")

async def setup(bot):
    await bot.add_cog(OCR(bot))