from flask import Flask
from threading import Thread
from dotenv import load_dotenv
from discord.ext import commands
import discord
import os
import aiosqlite

# Load environment variables from .env file
load_dotenv()

# Bot configuration
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = '.'
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

SPONSORS = [1234567890, 9876543210]  # List of sponsor user IDs

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    bot.db = await aiosqlite.connect('data/messages.db')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.author.id in SPONSORS:
        await message.channel.send(f"Thank you for sponsoring, {message.author.mention}!")

    async with bot.db.execute('INSERT INTO messages (user_id, message) VALUES (?, ?)', (message.author.id, message.content)):
        await bot.db.commit()
    await bot.process_commands(message)

# Load cogs
async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

# Flask web server to keep the bot running
app = Flask(__name__)

@app.route('/')
def home():
    return "Discord bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    keep_alive()
    bot.loop.create_task(load_cogs())
    bot.run(TOKEN)

@bot.event
async def on_close():
    await bot.db.close()