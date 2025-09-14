"""Command handlers for the bot."""

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold, hitalic

from src.types.models import User
from .base_handler import BaseHandler


class CommandHandler(BaseHandler):
    """Handler for bot commands."""
    
    def __init__(self):
        super().__init__()
        self.router = Router()
        self._register_handlers()
    
    def _register_handlers(self):
        """Register command handlers."""
        self.router.message(CommandStart())(self.start_command)
        self.router.message(Command("help"))(self.help_command)
        self.router.message(Command("search"))(self.search_command)
        self.router.message(Command("status"))(self.status_command)
    
    async def handle(self, message: Message, user: User, **kwargs):
        """Handle command messages."""
        context = await self.create_context(user, message=message)
        await self.log_handler_start("CommandHandler", context)
        
        try:
            # Router will automatically dispatch to the appropriate handler
            return await self.router.propagate_event("message", message, user=user, **kwargs)
        except Exception as e:
            await self.log_error("CommandHandler", e, context)
            raise
        finally:
            await self.log_handler_end("CommandHandler", context)
    
    async def start_command(self, message: Message, user: User):
        """Handle /start command."""
        welcome_text = (
            f"🤖 {hbold('Welcome to AutoSearcher Bot!')}\n\n"
            f"👋 Hello, {hbold(user.first_name or 'there')}!\n\n"
            f"I'm an AI-powered bot that helps you search for products across multiple marketplaces:\n"
            f"• 🛒 OZON\n"
            f"• 🟣 Wildberries\n"
            f"• 🟡 Yandex Market\n\n"
            f"🔍 To start searching, just type {hitalic('/search')} followed by your query!\n\n"
            f"📚 Use {hitalic('/help')} to see all available commands."
        )
        
        await message.answer(welcome_text)
    
    async def help_command(self, message: Message, user: User):
        """Handle /help command."""
        help_text = (
            f"📚 {hbold('Available Commands:')}\n\n"
            f"🏠 {hbold('/start')} - Start the bot and see welcome message\n"
            f"❓ {hbold('/help')} - Show this help message\n"
            f"🔍 {hbold('/search')} <query> - Search for products\n"
            f"📊 {hbold('/status')} - Check bot status\n\n"
            f"💡 {hbold('How to search:')}\n"
            f"Simply type {hitalic('/search laptop gaming')} to find gaming laptops!\n\n"
            f"🤖 I'll search across multiple marketplaces and show you the best results."
        )
        
        await message.answer(help_text)
    
    async def search_command(self, message: Message, user: User):
        """Handle /search command."""
        # Extract search query from command
        command_text = message.text or ""
        search_query = command_text.replace("/search", "").strip()
        
        if not search_query:
            await message.answer(
                "🔍 Please provide a search query!\n\n"
                f"Example: {hitalic('/search laptop gaming')}"
            )
            return
        
        # TODO: Integrate with search use case
        await message.answer(
            f"🔍 Searching for: {hbold(search_query)}\n\n"
            f"🤖 I'm analyzing your request and searching across marketplaces...\n"
            f"⏳ This may take a few moments."
        )
        
        # Placeholder for actual search implementation
        await message.answer(
            f"🚧 Search functionality is being implemented!\n"
            f"Your query: {hitalic(search_query)}"
        )
    
    async def status_command(self, message: Message, user: User):
        """Handle /status command."""
        status_text = (
            f"🤖 {hbold('Bot Status')}\n\n"
            f"✅ Bot is running\n"
            f"👤 User: {user.first_name or 'Unknown'} ({user.role})\n"
            f"🆔 User ID: {user.id}\n"
            f"💬 Chat ID: {message.chat.id}\n\n"
            f"🔧 All systems operational!"
        )
        
        await message.answer(status_text)