import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
PREFIX = '.'
TICKET_CATEGORY_ID = int(os.getenv('TICKET_CATEGORY_ID', '0'))
STAFF_ROLE_ID = int(os.getenv('STAFF_ROLE_ID', '0'))
LOG_CHANNEL_ID = int(os.getenv('LOG_CHANNEL_ID', '1308525133048188949'))

# URLs and Endpoints
BOT_WEBSITE = "https://drago-03.github.io/IndieGo-Website/"
SUPPORT_SERVER_LINK = "https://discord.gg/9bPsjgnJ5v"
INTERACTIONS_URL = f"{BOT_WEBSITE}/api/interactions"
LINKED_ROLES_URL = f"{BOT_WEBSITE}/api/linked-roles"
TERMS_URL = f"{BOT_WEBSITE}/terms"
PRIVACY_URL = f"{BOT_WEBSITE}/privacy"
INSTALL_URL = "https://discord.com/oauth2/authorize?client_id=1304755116255088670"
OAUTH2_URL = f"https://discord.com/api/oauth2/authorize?client_id=1304755116255088670&redirect_uri={BOT_WEBSITE}/callback&response_type=code&scope=identify%20guilds"

# Branding
EMBED_COLOR = 0x9F7AEA  # Purple
AUTHOR_NAME = "Built by Drago"
AUTHOR_ICON = "https://your-domain.com/assets/drago-icon.png"