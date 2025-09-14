"""Base handler class for bot handlers."""

from abc import ABC, abstractmethod
from typing import Any, Dict

from aiogram.types import Message, CallbackQuery
from loguru import logger

from src.types.models import User, BotContext


class BaseHandler(ABC):
    """Base class for all bot handlers."""
    
    def __init__(self):
        self.logger = logger
    
    async def create_context(
        self,
        user: User,
        message: Message = None,
        callback_query: CallbackQuery = None,
        **kwargs
    ) -> BotContext:
        """Create bot context from message or callback query."""
        
        chat_id = None
        message_id = None
        callback_data = None
        text = None
        
        if message:
            chat_id = message.chat.id
            message_id = message.message_id
            text = message.text
            
        elif callback_query:
            if callback_query.message:
                chat_id = callback_query.message.chat.id
                message_id = callback_query.message.message_id
            callback_data = callback_query.data
        
        return BotContext(
            user=user,
            chat_id=chat_id,
            message_id=message_id,
            callback_data=callback_data,
            text=text,
            metadata=kwargs
        )
    
    async def log_handler_start(self, handler_name: str, context: BotContext):
        """Log handler execution start."""
        self.logger.info(
            f"Handler {handler_name} started for user {context.user.id} "
            f"in chat {context.chat_id}"
        )
    
    async def log_handler_end(self, handler_name: str, context: BotContext):
        """Log handler execution end."""
        self.logger.info(
            f"Handler {handler_name} completed for user {context.user.id}"
        )
    
    async def log_error(self, handler_name: str, error: Exception, context: BotContext):
        """Log handler error."""
        self.logger.error(
            f"Handler {handler_name} failed for user {context.user.id}: {str(error)}",
            exc_info=True
        )
    
    @abstractmethod
    async def handle(self, *args, **kwargs) -> Any:
        """Handle the incoming event. Must be implemented by subclasses."""
        pass