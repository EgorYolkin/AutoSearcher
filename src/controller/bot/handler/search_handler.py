"""Search handlers for the bot."""

from aiogram import Router
from aiogram.types import Message
from aiogram.utils.markdown import hbold, hitalic

from src.types.models import User, MarketPlace
from .base_handler import BaseHandler


class SearchHandler(BaseHandler):
    """Handler for search-related messages."""
    
    def __init__(self):
        super().__init__()
        self.router = Router()
        self._register_handlers()
    
    def _register_handlers(self):
        """Register search handlers."""
        # Handle regular text messages as potential search queries
        self.router.message()(self.handle_text_message)
    
    async def handle(self, message: Message, user: User, **kwargs):
        """Handle search messages."""
        context = await self.create_context(user, message=message)
        await self.log_handler_start("SearchHandler", context)
        
        try:
            # Check if this is a search query
            if await self._is_search_query(message):
                return await self.handle_search_query(message, user)
            else:
                return await self.handle_general_message(message, user)
        except Exception as e:
            await self.log_error("SearchHandler", e, context)
            raise
        finally:
            await self.log_handler_end("SearchHandler", context)
    
    async def handle_text_message(self, message: Message, user: User):
        """Handle incoming text messages."""
        return await self.handle(message, user)
    
    async def _is_search_query(self, message: Message) -> bool:
        """Determine if the message is a search query."""
        text = message.text or ""
        
        # Skip if it's a command
        if text.startswith("/"):
            return False
        
        # Simple heuristics to detect search queries
        search_keywords = [
            "найти", "поиск", "ищу", "нужен", "купить", "где купить",
            "find", "search", "looking for", "need", "buy", "where to buy"
        ]
        
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in search_keywords) or len(text) > 3
    
    async def handle_search_query(self, message: Message, user: User):
        """Handle search query messages."""
        query_text = message.text or ""
        
        await message.answer(
            f"🔍 {hbold('Starting search...')}\n\n"
            f"Query: {hitalic(query_text)}\n"
            f"🛒 Searching across all marketplaces..."
        )
        
        # TODO: Integrate with AI use case and search services
        # For now, show a mock response
        marketplaces = [MarketPlace.OZON, MarketPlace.WILDBERRIES, MarketPlace.YANDEX_MARKET]
        
        response_text = (
            f"🤖 {hbold('AI Analysis Complete!')}\n\n"
            f"📝 Your query: {hitalic(query_text)}\n"
            f"🎯 Detected intent: Product search\n"
            f"🛒 Searching in: {', '.join([mp.value for mp in marketplaces])}\n\n"
            f"⏳ Fetching results..."
        )
        
        await message.answer(response_text)
        
        # Mock search results
        await self._send_mock_results(message, query_text)
    
    async def handle_general_message(self, message: Message, user: User):
        """Handle general messages that are not search queries."""
        await message.answer(
            f"👋 Hi! I'm a search bot.\n\n"
            f"🔍 To search for products, try:\n"
            f"• {hitalic('найти игровой ноутбук')}\n"
            f"• {hitalic('/search wireless headphones')}\n"
            f"• {hitalic('ищу смартфон до 30000')}\n\n"
            f"📚 Use {hitalic('/help')} for more commands."
        )
    
    async def _send_mock_results(self, message: Message, query: str):
        """Send mock search results."""
        # This is a placeholder for actual search results
        results_text = (
            f"✅ {hbold('Search Results Found!')}\n\n"
            f"🛒 {hbold('OZON:')} 15 products found\n"
            f"🟣 {hbold('Wildberries:')} 12 products found\n"
            f"🟡 {hbold('Yandex Market:')} 8 products found\n\n"
            f"💰 Price range: 5,000 - 50,000 ₽\n"
            f"⭐ Average rating: 4.3/5\n\n"
            f"🚧 {hitalic('Detailed results will be shown once the search engine is implemented.')}"
        )
        
        await message.answer(results_text)