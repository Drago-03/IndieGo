# Discord Developer Community Bot

A feature-rich Discord bot designed for developer communities with moderation, ticket system, coding help, and fun utilities.

## Features

- **Moderation Commands**
  - Kick/Ban users
  - Clear messages
  - Timeout users

- **Ticket System**
  - Create support tickets
  - Private channels for each ticket
  - Close tickets when resolved

- **Coding Help**
  - AI-powered coding assistance
  - Code explanations
  - Programming help

- **Fun Utilities**
  - Dice rolling
  - Choice maker
  - Programming jokes
  - Poll creation

## Setup

1. Create a `.env` file based on `.env.example`
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the bot:
   ```bash
   python bot.py
   ```

## Commands

- `!kick @user [reason]` - Kick a user
- `!ban @user [reason]` - Ban a user
- `!clear [amount]` - Clear messages
- `!timeout @user [minutes] [reason]` - Timeout a user
- `!ticket` - Create a support ticket
- `!close` - Close a ticket
- `!codehelp [question]` - Get coding help
- `!roll NdN` - Roll dice
- `!choose [options]` - Choose between options
- `!joke` - Tell a programming joke
- `!poll [question] [options]` - Create a poll