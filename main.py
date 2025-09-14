"""Main entry point for the AI-agent telegram bot."""

import asyncio
import sys
from pathlib import Path

from loguru import logger

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.app.app import create_application
from src.config.config import settings


async def main():
    """Main function to run the bot."""
    
    logger.info("Starting AutoSearcher AI-agent telegram bot...")
    
    try:
        # Create application
        app = await create_application()
        
        # Choose deployment mode
        if settings.bot.webhook_url:
            # Production mode with webhook
            logger.info("Running in webhook mode")
            await app.setup_webhook(
                webhook_url=settings.bot.webhook_url,
                webhook_path=settings.bot.webhook_path
            )
            
            # In webhook mode, the application would typically run in a web server
            # For this example, we'll just keep the application alive
            logger.info("Webhook setup complete. Bot is ready to receive updates.")
            
            # Keep the application running
            try:
                while True:
                    await asyncio.sleep(60)
                    
                    # Perform periodic health checks
                    if not await app.health_check():
                        logger.error("Health check failed")
                        break
                        
            except KeyboardInterrupt:
                logger.info("Received interrupt signal")
        else:
            # Development mode with polling
            logger.info("Running in polling mode")
            await app.start_polling()
    
    except Exception as e:
        logger.error(f"Application failed to start: {str(e)}")
        return 1
    
    finally:
        # Cleanup
        if 'app' in locals():
            await app.shutdown()
    
    return 0


if __name__ == "__main__":
    # Ensure logs directory exists
    Path("logs").mkdir(exist_ok=True)
    
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}")
        sys.exit(1)