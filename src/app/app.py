"""Application factory for the AI-agent telegram bot."""

import asyncio
from typing import Optional

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from loguru import logger

from src.config.config import settings
from src.controller.bot.handler import CommandHandler, SearchHandler, CallbackHandler
from src.controller.bot.middleware import AuthMiddleware, LoggingMiddleware, RateLimitMiddleware


class Application:
    """Main application class for the telegram bot."""
    
    def __init__(self):
        self.bot: Optional[Bot] = None
        self.dispatcher: Optional[Dispatcher] = None
        self._setup_logging()
    
    def _setup_logging(self):
        """Configure logging for the application."""
        logger.add(
            "logs/bot.log",
            rotation="1 day",
            retention="7 days",
            level=settings.app.log_level,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}"
        )
        
        if settings.app.debug:
            logger.add(
                "logs/debug.log",
                level="DEBUG",
                format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}"
            )
    
    async def create_bot(self) -> Bot:
        """Create and configure the bot instance."""
        
        bot = Bot(
            token=settings.bot.token,
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML
            )
        )
        
        # Verify bot token
        try:
            bot_info = await bot.get_me()
            logger.info(f"Bot initialized: @{bot_info.username} ({bot_info.full_name})")
        except Exception as e:
            logger.error(f"Failed to initialize bot: {str(e)}")
            raise
        
        self.bot = bot
        return bot
    
    def create_dispatcher(self) -> Dispatcher:
        """Create and configure the dispatcher."""
        
        dispatcher = Dispatcher()
        
        # Register middleware
        self._register_middleware(dispatcher)
        
        # Register handlers
        self._register_handlers(dispatcher)
        
        self.dispatcher = dispatcher
        return dispatcher
    
    def _register_middleware(self, dispatcher: Dispatcher):
        """Register middleware with the dispatcher."""
        
        # Register middleware in order of execution
        dispatcher.message.middleware(LoggingMiddleware())
        dispatcher.callback_query.middleware(LoggingMiddleware())
        
        dispatcher.message.middleware(AuthMiddleware())
        dispatcher.callback_query.middleware(AuthMiddleware())
        
        dispatcher.message.middleware(RateLimitMiddleware(rate_limit=10, window=60))
        
        logger.info("Middleware registered")
    
    def _register_handlers(self, dispatcher: Dispatcher):
        """Register handlers with the dispatcher."""
        
        # Create handler instances
        command_handler = CommandHandler()
        search_handler = SearchHandler()
        callback_handler = CallbackHandler()
        
        # Register routers
        dispatcher.include_router(command_handler.router)
        dispatcher.include_router(callback_handler.router)
        dispatcher.include_router(search_handler.router)  # Should be last to catch general messages
        
        logger.info("Handlers registered")
    
    async def setup_webhook(self, webhook_url: str, webhook_path: str = "/webhook"):
        """Setup webhook for production deployment."""
        
        if not self.bot:
            raise RuntimeError("Bot not initialized")
        
        try:
            # Set webhook
            await self.bot.set_webhook(
                url=f"{webhook_url}{webhook_path}",
                drop_pending_updates=True
            )
            
            logger.info(f"Webhook set to {webhook_url}{webhook_path}")
            
        except Exception as e:
            logger.error(f"Failed to setup webhook: {str(e)}")
            raise
    
    async def start_polling(self):
        """Start polling for updates (development mode)."""
        
        if not self.bot or not self.dispatcher:
            raise RuntimeError("Bot and dispatcher must be initialized")
        
        logger.info("Starting polling...")
        
        try:
            # Delete webhook if it exists
            await self.bot.delete_webhook(drop_pending_updates=True)
            
            # Start polling
            await self.dispatcher.start_polling(self.bot)
            
        except Exception as e:
            logger.error(f"Polling failed: {str(e)}")
            raise
    
    async def shutdown(self):
        """Shutdown the application gracefully."""
        
        logger.info("Shutting down application...")
        
        if self.dispatcher:
            await self.dispatcher.stop_polling()
        
        if self.bot:
            await self.bot.session.close()
        
        logger.info("Application shutdown complete")
    
    async def health_check(self) -> bool:
        """Perform health check."""
        
        try:
            if not self.bot:
                return False
            
            # Test bot connectivity
            await self.bot.get_me()
            return True
            
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return False


async def create_application() -> Application:
    """Factory function to create and setup the application."""
    
    app = Application()
    
    # Create bot and dispatcher
    await app.create_bot()
    app.create_dispatcher()
    
    logger.info("Application created successfully")
    
    return app