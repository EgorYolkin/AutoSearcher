from aiogram import types, Router
from aiogram.filters import Command

handle_start_cmd_router = Router()

START_CMD_ANSWER = "Send me a voice messages"


@handle_start_cmd_router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(START_CMD_ANSWER)
