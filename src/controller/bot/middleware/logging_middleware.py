"""Logging middleware for the bot."""

import time
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update
from loguru import logger


class LoggingMiddleware(BaseMiddleware):
    """Middleware for logging bot activities."""
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        """Log incoming events and handler execution time."""
        
        start_time = time.time()
        
        # Log incoming event
        if isinstance(event, Update):
            await self._log_update(event, data)
        
        try:
            # Execute handler
            result = await handler(event, data)
            
            # Log successful execution
            execution_time = time.time() - start_time
            logger.info(
                f"Handler executed successfully in {execution_time:.3f}s"
            )
            
            return result
            
        except Exception as e:
            # Log error
            execution_time = time.time() - start_time
            logger.error(
                f"Handler failed after {execution_time:.3f}s: {str(e)}",
                exc_info=True
            )
            raise
    
    async def _log_update(self, update: Update, data: Dict[str, Any]) -> None:
        """Log details about the incoming update."""
        
        user_info = "unknown"
        content_info = "unknown"
        
        # Extract user information
        if update.message:
            user = update.message.from_user
            if user:
                user_info = f"{user.id}:{user.username or user.first_name}"
            
            # Extract content information
            if update.message.text:
                content_info = f"text: {update.message.text[:50]}"
            elif update.message.photo:
                content_info = "photo"
            elif update.message.document:
                content_info = "document"
            elif update.message.voice:
                content_info = "voice"
            else:
                content_info = "other_message_type"
                
        elif update.callback_query:
            user = update.callback_query.from_user
            if user:
                user_info = f"{user.id}:{user.username or user.first_name}"
            content_info = f"callback: {update.callback_query.data}"
            
        elif update.inline_query:
            user = update.inline_query.from_user
            if user:
                user_info = f"{user.id}:{user.username or user.first_name}"
            content_info = f"inline: {update.inline_query.query}"
        
        logger.info(f"Update from {user_info} - {content_info}")