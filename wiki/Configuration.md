# Configuration Guide

This document details all configuration options for the DevAssist Discord bot.

## Environment Variables

### Required Variables

```env
DISCORD_TOKEN=your_discord_token_here
OPENAI_API_KEY=your_openai_api_key_here
```

### Optional Variables

```env
LOG_LEVEL=INFO
DATABASE_PATH=data/subscriptions.db
TICKET_CATEGORY_ID=123456789
STAFF_ROLE_ID=987654321
```

## Configuration Files

### 1. Premium Features (`src/config/premium_features.json`)

Controls subscription tiers and their features:

```json
{
  "tiers": {
    "free": {
      "code_reviews_per_day": 5,
      "ai_responses_per_day": 10
    },
    "pro": {
      "price_monthly": 9.99,
      "code_reviews_per_day": 20
    },
    "enterprise": {
      "price_monthly": 29.99,
      "code_reviews_per_day": "unlimited"
    }
  }
}
```

### 2. Project Templates (`src/config/project_templates.json`)

Defines project scaffolding templates:

```json
{
  "python-web": {
    "name": "Python Web Application",
    "description": "FastAPI web application template",
    "structure": [...]
  }
}
```

### 3. Commands (`src/config/commands.json`)

Configures command settings:

```json
{
  "categories": {
    "programming": {
      "code_review": {
        "cooldown": 60,
        "premium_only": false
      }
    }
  }
}
```

## Discord Configuration

### Bot Permissions

Required permissions integer: `8`

Includes:

- Manage Messages
- Manage Channels
- View Channels
- Send Messages
- Embed Links
- Attach Files
- Read Message History
- Add Reactions

### Intents

Required intents:

- Message Content
- Guild Members
- Guild Messages
- Guild Message Reactions

## Database Configuration

Default SQLite database location: `data/subscriptions.db`

Custom location:

```python
subscription = Subscription(db_path="custom/path/to/db.sqlite")
```

## Logging Configuration

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
```

## Security Considerations

1. Token Security
   - Never commit tokens to repository
   - Rotate tokens regularly
   - Use environment variables

2. Permission Management
   - Implement role-based access
   - Restrict sensitive commands
   - Regular permission audits

3. Rate Limiting
   - Implement cooldowns
   - Monitor API usage
   - Prevent abuse

## Advanced Configuration

### Custom Analyzers

Create custom code analyzers:

```python
class CustomAnalyzer(CodeAnalyzer):
    def __init__(self):
        super().__init__()
        self.custom_rules = [...]
```

### Command Customization

Add custom commands:

```python
@commands.command()
async def custom_command(self, ctx):
    # Implementation
    pass
```
