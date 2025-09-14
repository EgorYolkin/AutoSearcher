# AutoSearcher

Simple Telegram bot to search products. Now it works with Wildberries links. You send a category link. The bot gets products from this category and sends short info back.

Note: Ozon and Yandex Market are future plans. Today the bot only uses Wildberries.

## Features

- Simple Telegram bot: you chat with the bot.
- Send a Wildberries category URL; bot returns product list.
- Shows name, price, old price, rating, reviews, and link.
- Safe defaults: the bot limits items it sends in one message.

## Requirements

- Python `3.13` (or close version).
- Telegram Bot API token from BotFather.
- macOS, Linux, or Windows.
- Optional: Docker and Docker Compose.

## Project Structure

- `main.py`: start the app.
- `src/app/app.py`: create bot and run polling.
- `src/controller/bot/handler/handle_start_cmd.py`: `/start` command.
- `src/controller/bot/handler/handle_parse.py`: handle Wildberries links.
- `src/service/wb_parse_service.py`: get products from Wildberries API.
- `src/types/wb_parser.py`: product data model.
- `configs/.env`: your secrets (create this file).
- `infra/docker/`: Docker files.

## Setup

1) Create a bot in Telegram
- Open Telegram and talk to `@BotFather`.
- Send `/newbot` and follow the steps.
- Copy the token. It looks like `123456789:ABC-DEF...`.

2) Create env file
- Copy `configs/.env.dist` to `configs/.env`.
- Put your token in it:

```
TELEGRAM_BOT_API_KEY=123456789:YOUR-BOT-TOKEN
```

3) Create virtual environment (macOS/Linux)

```
python3 -m venv env
. env/bin/activate
python3 -m pip install -r requirements.txt
```

On Windows (PowerShell):

```
py -m venv env
./env/Scripts/Activate.ps1
py -m pip install -r requirements.txt
```

## Run

Start the bot:

```
python3 main.py
```

You should see logs in your console. If the token is wrong, the app stops.

## Run with Docker

Option A — Simple Docker build/run:

```
# from project root
docker build -f infra/docker/Dockerfile -t auto-searcher-bot .
docker run --env-file configs/.env --name auto-searcher-bot --rm auto-searcher-bot
```

Option B — Docker Compose (may need context fix):

```
# from project root
docker compose -f infra/docker/docker-compose.yml up --build
```

Note: The compose file uses a local build context. If the image does not include the app code, use Option A.

## How to Use

1) Open your bot in Telegram.
2) Send `/start`. The bot says hello.
3) Send a Wildberries category link. Example:

```
https://www.wildberries.ru/catalog/sport/vidy-sporta/velosport/velosipedy
```

The bot starts work. It says it is collecting products. Then it sends a list of items. For each item it shows:
- Name
- Price and old price
- Rating and number of reviews
- Link to the product

Tip: The bot now uses simple default filters inside the code (price range and discount). You can change them later in `src/controller/bot/handler/handle_parse.py`.

## Troubleshooting

- Bot does not start: check `configs/.env` and your token.
- No reply in chat: check internet, then restart the bot.
- “Category not found”: send a valid Wildberries category link.
- Too long answer: the bot splits results, but very big lists can still be slow.

## Development

- Code style: simple and clear. Focus on the `src/` folder.
- Main files to read:
  - `src/app/app.py` (start logic)
  - `src/controller/bot/handler/*` (message handlers)
  - `src/service/wb_parse_service.py` (data fetch)

Run tests: there are no tests now.

## License

See `LICENSE`.
