"""Rate limiting middleware for the bot."""

import time
from collections import defaultdict
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update
from loguru import logger


class RateLimitMiddleware(BaseMiddleware):
    """Middleware for rate limiting user requests."""
    
    def __init__(self, rate_limit: int = 5, window: int = 60):
        """
        Initialize rate limiter.
        
        Args:
            rate_limit: Maximum number of requests per window
            window: Time window in seconds
        """
        super().__init__()
        self.rate_limit = rate_limit
        self.window = window
        self.user_requests = defaultdict(list)
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        """Check rate limits before processing the event."""
        
        if not isinstance(event, Update):
            return await handler(event, data)
        
        # Get user ID
        user_id = self._get_user_id(event)
        if not user_id:
            return await handler(event, data)
        
        # Check rate limit
        current_time = time.time()
        if await self._is_rate_limited(user_id, current_time):
            logger.warning(f"Rate limit exceeded for user {user_id}")
            
            # Send rate limit message if it's a message update
            if event.message and event.message.chat:
                from aiogram import Bot
                bot: Bot = data.get("bot")
                if bot:
                    await bot.send_message(
                        chat_id=event.message.chat.id,
                        text="⚠️ You're sending messages too quickly. Please wait a moment."
                    )
            
            return None
        
        # Record this request
        self.user_requests[user_id].append(current_time)
        
        return await handler(event, data)
    
    def _get_user_id(self, update: Update) -> int | None:
        """Extract user ID from update."""
        
        if update.message:
            return update.message.from_user.id if update.message.from_user else None
        elif update.callback_query:
            return update.callback_query.from_user.id if update.callback_query.from_user else None
        elif update.inline_query:
            return update.inline_query.from_user.id if update.inline_query.from_user else None
        
        return None
    
    async def _is_rate_limited(self, user_id: int, current_time: float) -> bool:
        """Check if user is rate limited."""
        
        # Get user's request history
        requests = self.user_requests[user_id]
        
        # Remove requests outside the time window
        cutoff_time = current_time - self.window
        requests[:] = [req_time for req_time in requests if req_time > cutoff_time]
        
        # Check if user has exceeded the rate limit
        return len(requests) >= self.rate_limit