import logging
from aiogram import BaseMiddleware, types

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

USER_MESSAGE_RECEIVED_LOG_MESSAGE = f"received message from user: %s - %s"
BOT_MESSAGE_SENT_LOG_MESSAGE = f"bot message sent: %s - %s"


class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):

        # internal message
        if isinstance(event, types.Message):
            logger.info(
                USER_MESSAGE_RECEIVED_LOG_MESSAGE %
                (event.from_user.id, event.text),
            )

        result = await handler(event, data)

        # external message
        if isinstance(result, types.Message):
            logger.info(
                BOT_MESSAGE_SENT_LOG_MESSAGE %
                (result.from_user.id, result.text)
            )

        return result
