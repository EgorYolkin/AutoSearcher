import typing
import logging
from aiogram import Bot, Dispatcher

from src.config.config import load_config_from_env
from src.controller.bot.handler.handle_parse import handle_parse_router
from src.controller.bot.handler.handle_start_cmd import handle_start_cmd_router


async def run_app(
        env_file_path: str,
):
    """
        Provide function for app running
    """

    cfg = load_config_from_env(
        env_file_path=env_file_path,
    )

    if not cfg:
        return

    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=cfg.telegram_bot_api_key)
    dp = Dispatcher()

    dp = register_handlers(dp)

    await dp.start_polling(bot)


def register_handlers(dp: Dispatcher) -> Dispatcher:
    dp.include_router(handle_start_cmd_router)
    dp.include_router(handle_parse_router)

    return dp
