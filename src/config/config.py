import dataclasses
import logging
import os

import dotenv

ENV_TELEGRAM_BOT_API_KEY = "TELEGRAM_BOT_API_KEY"


@dataclasses.dataclass
class Config:
    """
        Provide global configuration for app
    """

    telegram_bot_api_key: str


def load_config_from_env(
        env_file_path: str,
) -> Config | None:
    is_successfully = dotenv.load_dotenv(
        dotenv_path=env_file_path,
    )

    if not is_successfully:
        logging.error(ENV_TELEGRAM_BOT_API_KEY)
        return None

    config = Config(
        telegram_bot_api_key=os.getenv(ENV_TELEGRAM_BOT_API_KEY),
    )

    return config
