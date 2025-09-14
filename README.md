# AutoSearcher

LangChain LLM Agent for products search on OZON, Wildberries and Yandex Market

## Overview

AutoSearcher is an AI-powered Telegram bot that helps users search for products across multiple Russian marketplaces including OZON, Wildberries, and Yandex Market. The bot uses aiogram framework for Telegram integration and LangChain for AI capabilities.

## Architecture

```
├── configs/               # Configuration files
│   ├── .env.example      # Environment variables template
│   └── __init__.py
├── main.py               # Application entry point
├── requirements.txt      # Python dependencies
└── src/
    ├── app/
    │   └── app.py        # Application factory
    ├── config/
    │   └── config.py     # Configuration management
    ├── controller/
    │   └── bot/
    │       ├── handler/  # Bot message handlers
    │       └── middleware/  # Bot middleware
    ├── types/
    │   ├── app.py       # Application types
    │   └── models.py    # Data models
    └── usecase/
        ├── ai_agent_use_case.py  # AI/LLM logic
        └── search_use_case.py    # Product search logic
```

## Features

- 🤖 AI-powered natural language understanding
- 🔍 Multi-marketplace product search
- 📊 Price comparison across platforms
- ⚡ Async processing for fast responses
- 🛡️ Rate limiting and authentication
- 📝 Comprehensive logging
- 🔧 Configurable settings

## Installation

1. Clone the repository:
```bash
git clone https://github.com/EgorYolkin/AutoSearcher.git
cd AutoSearcher
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp configs/.env.example .env
# Edit .env with your configuration
```

4. Run the bot:
```bash
python main.py
```

## Configuration

Create a `.env` file based on `.env.example`:

```env
# Required
BOT_TOKEN=your_telegram_bot_token_here

# Optional AI features
OPENAI_API_KEY=your_openai_api_key_here

# Optional settings
DEBUG=True
LOG_LEVEL=INFO
```

## Bot Commands

- `/start` - Start the bot and see welcome message
- `/help` - Show help message with available commands
- `/search <query>` - Search for products across marketplaces
- `/status` - Check bot status

## Usage Examples

1. **Simple search:**
   ```
   /search gaming laptop
   ```

2. **Natural language search:**
   ```
   ищу смартфон до 30000 рублей
   ```

3. **Product comparison:**
   ```
   найти беспроводные наушники
   ```

## Development

### Project Structure

The project follows a clean architecture pattern:

- **Handlers**: Process incoming Telegram messages
- **Middleware**: Handle cross-cutting concerns (auth, logging, rate limiting)
- **Use Cases**: Contain business logic
- **Models**: Define data structures
- **Config**: Manage application settings

### Adding New Features

1. **New Commands**: Add handlers in `src/controller/bot/handler/`
2. **AI Features**: Extend `src/usecase/ai_agent_use_case.py`
3. **Marketplace Integration**: Extend `src/usecase/search_use_case.py`

### Testing

```bash
python -m pytest tests/
```

## Deployment

### Development (Polling)
```bash
python main.py
```

### Production (Webhook)
Set `WEBHOOK_URL` in your environment and deploy to a server that supports HTTPS.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.
