# Installation Guide

This guide provides detailed instructions for setting up the DevAssist Discord bot.

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- A Discord account and application
- Gemini and Anthropic Api key

## Step-by-Step Installation

### 1. System Requirements

#### Windows
- Install Python from [python.org](https://python.org)
- Add Python to PATH during installation
- Install Git from [git-scm.com](https://git-scm.com)

#### Linux/macOS
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip git

# macOS (using Homebrew)
brew install python git
```

### 2. Clone Repository

```bash
git clone https://github.com/Drago-03/IndieGo.git
cd IndieGo
```

### 3. Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configuration

1. Copy example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your credentials:
   ```env
   DISCORD_TOKEN=your_discord_token_here
   GEMINI_API_KEY=api_key_here
   ANTHROPIC_API_KEY=API_KEY_HERE
   ```

3. Configure `config.py`:
   - Adjust settings as needed
   - Add team members list

### 6. Database Setup

```bash
python scripts/init_db.py
```

### 7. Run Tests

```bash
pytest tests/
```

### 8. Start the Bot

```bash
python src/main.py
```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**
   - Ensure virtual environment is activated
   - Verify all dependencies are installed
   ```bash
   pip install -r requirements.txt --upgrade
   ```

2. **Discord Token Invalid**
   - Check token in Discord Developer Portal
   - Ensure token is correctly copied to `.env`

3. **Database Errors**
   - Delete existing database file
   - Run initialization script again
   ```bash
   rm data/subscriptions.db
   python scripts/init_db.py
   ```

### Getting Help

- Check [FAQ](FAQ.md)
- Join our [Discord server](https://discord.gg/9bPsjgnJ5v)
- Open an [issue](https://github.com/Drago-03/IndieGO/issues)