import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PREFIX = '!'
TICKET_CATEGORY_ID = None
STAFF_ROLE_ID = None

# URLs and Endpoints
BOT_WEBSITE = "https://devassist-bot.netlify.app"
INTERACTIONS_URL = f"{BOT_WEBSITE}/api/interactions"
LINKED_ROLES_URL = f"{BOT_WEBSITE}/api/linked-roles"
TERMS_URL = f"{BOT_WEBSITE}/terms"
PRIVACY_URL = f"{BOT_WEBSITE}/privacy"
INSTALL_URL = f"https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=8&scope=bot%20applications.commands"
OAUTH2_URL = f"https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&redirect_uri={BOT_WEBSITE}/callback&response_type=code&scope=identify%20guilds"

# Branding
EMBED_COLOR = 0x9F7AEA  # Purple
AUTHOR_NAME = "Built by Drago"
AUTHOR_ICON = "https://your-domain.com/assets/drago-icon.png"