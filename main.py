import asyncio

from src.app.app import run_app

ENV_FILE_PATH = "configs/.env"

if __name__ == "__main__":
    asyncio.run(run_app(
        env_file_path=ENV_FILE_PATH,
    ))
