"""Authentication middleware for the bot."""

from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update, User as AiogramUser
from loguru import logger

from src.config.config import settings
from src.types.models import User, UserRole


class AuthMiddleware(BaseMiddleware):
    """Middleware for user authentication and authorization."""
    
    def __init__(self):
        super().__init__()
        self.admin_ids = set(settings.bot.admin_ids)
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        """Process authentication for incoming events."""
        
        if not isinstance(event, Update):
            return await handler(event, data)
        
        # Get user from update
        aiogram_user = None
        if event.message:
            aiogram_user = event.message.from_user
        elif event.callback_query:
            aiogram_user = event.callback_query.from_user
        elif event.inline_query:
            aiogram_user = event.inline_query.from_user
        
        if not aiogram_user:
            logger.warning("No user found in update")
            return await handler(event, data)
        
        # Create user model
        user = await self._get_or_create_user(aiogram_user)
        
        # Add user to handler data
        data["user"] = user
        data["is_admin"] = user.role == UserRole.ADMIN
        
        # Log user activity
        logger.info(
            f"User {user.id} ({user.username or 'no_username'}) "
            f"with role {user.role} is making request"
        )
        
        return await handler(event, data)
    
    async def _get_or_create_user(self, aiogram_user: AiogramUser) -> User:
        """Get or create user from aiogram user."""
        
        # Determine user role
        role = UserRole.ADMIN if aiogram_user.id in self.admin_ids else UserRole.USER
        
        # Create user model
        user = User(
            id=aiogram_user.id,
            username=aiogram_user.username,
            first_name=aiogram_user.first_name,
            last_name=aiogram_user.last_name,
            role=role
        )
        
        # TODO: In a real application, this would involve database operations
        # For now, we just return the user model
        
        return user