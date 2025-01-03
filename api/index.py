from flask import Flask, request
import os
import discord
from discord.ext import commands
from threading import Thread

app = Flask(__name__)

# Load environment variables
TOKEN = os.getenv('DISCORD_TOKEN')

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@app.route('/')
def home():
    return "Discord bot is running!"

def run_bot():
    bot.run(TOKEN)

# Start the bot in a separate thread
thread = Thread(target=run_bot)
thread.start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)