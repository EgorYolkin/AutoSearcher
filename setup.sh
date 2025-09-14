#!/bin/bash

# AutoSearcher Bot Quick Start Script

echo "🤖 AutoSearcher Bot Quick Start"
echo "================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

echo "✓ Python 3 found"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed"
    exit 1
fi

echo "✓ pip3 found"

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️  Creating .env file..."
    cp configs/.env.example .env
    echo "✓ .env file created from template"
    echo "📝 Please edit .env file with your bot token and other settings"
    echo
else
    echo "✓ .env file already exists"
fi

# Create logs directory
mkdir -p logs
echo "✓ Logs directory created"

echo
echo "🎉 Setup complete!"
echo
echo "Next steps:"
echo "1. Edit .env file with your Telegram bot token"
echo "2. Run the bot: python3 main.py"
echo
echo "For development with auto-reload:"
echo "pip3 install watchdog"
echo "python3 -m watchdog.tricks shell_command --patterns='*.py' --recursive 'python3 main.py'"
echo