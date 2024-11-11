import discord
from discord.ext import commands
import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

class CodingHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def code(self, ctx, *, question):
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
                    await ctx.send(f"```{chunk}```")
            else:
                await ctx.send(f"```{answer}```")
                
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

    @commands.command()
    async def explain(self, ctx, *, code):
        try:
            response = await openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful coding assistant. Explain the provided code in simple terms."},
                    {"role": "user", "content": f"Explain this code: {code}"}
                ]
            )
            
            await ctx.send(response.choices[0].message.content)
            
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

async def setup(bot):
    await bot.add_cog(CodingHelp(bot))