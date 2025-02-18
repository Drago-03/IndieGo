import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot Configuration
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('COMMAND_PREFIX', '!')  # Default prefix is ! if not specified
LOG_CHANNEL_ID = int(os.getenv('LOG_CHANNEL_ID', '1308525133048188949'))

# URLs and Endpoints
BOT_WEBSITE = "https://drago-03.github.io/IndieGo-Website/"
SUPPORT_SERVER_LINK = "https://discord.gg/9bPsjgnJ5v"
INSTALL_URL = "https://discord.com/oauth2/authorize?client_id=1304755116255088670&permissions=8&scope=bot%20applications.commands"
OAUTH2_URL = f"https://discord.com/oauth2/authorize?client_id=1304755116255088670&redirect_uri={BOT_WEBSITE}/callback&response_type=code&scope=identify%20guilds"

# API Endpoints
INTERACTIONS_URL = f"{BOT_WEBSITE}/api/interactions"
LINKED_ROLES_URL = f"{BOT_WEBSITE}/api/linked-roles"
TERMS_URL = f"{BOT_WEBSITE}/terms"
PRIVACY_URL = f"{BOT_WEBSITE}/privacy"

# Branding
EMBED_COLOR = 0x9F7AEA  # Purple
AUTHOR_NAME = "Built by Drago | Product of Indie Hub"
AUTHOR_ICON = f"{BOT_WEBSITE}/assets/logo.png"
INDIE_HUB_LINK = "https://discord.gg/9bPsjgnJ5v"

# Command Settings
COOLDOWN_TIME = 3  # seconds
MAX_WARNINGS = 3
DEFAULT_DELETE_DAYS = 7

# Logging
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = 'bot.log'

# Copyright and Attribution
COPYRIGHT = "© 2025 Indie Hub. All rights reserved."
ATTRIBUTION = "A product of Indie Hub - Empowering Independent Developers"