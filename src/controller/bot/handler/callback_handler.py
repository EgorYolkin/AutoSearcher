"""Callback query handlers for the bot."""

from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold

from src.types.models import User
from .base_handler import BaseHandler


class CallbackHandler(BaseHandler):
    """Handler for callback queries (inline keyboard interactions)."""
    
    def __init__(self):
        super().__init__()
        self.router = Router()
        self._register_handlers()
    
    def _register_handlers(self):
        """Register callback handlers."""
        self.router.callback_query()(self.handle_callback)
    
    async def handle(self, callback_query: CallbackQuery, user: User, **kwargs):
        """Handle callback queries."""
        context = await self.create_context(user, callback_query=callback_query)
        await self.log_handler_start("CallbackHandler", context)
        
        try:
            return await self.handle_callback(callback_query, user)
        except Exception as e:
            await self.log_error("CallbackHandler", e, context)
            raise
        finally:
            await self.log_handler_end("CallbackHandler", context)
    
    async def handle_callback(self, callback_query: CallbackQuery, user: User):
        """Handle callback query."""
        data = callback_query.data or ""
        
        # Always acknowledge the callback to remove loading state
        await callback_query.answer()
        
        if data.startswith("search_"):
            await self._handle_search_callback(callback_query, data)
        elif data.startswith("product_"):
            await self._handle_product_callback(callback_query, data)
        elif data.startswith("marketplace_"):
            await self._handle_marketplace_callback(callback_query, data)
        elif data.startswith("filter_"):
            await self._handle_filter_callback(callback_query, data)
        else:
            await self._handle_unknown_callback(callback_query, data)
    
    async def _handle_search_callback(self, callback_query: CallbackQuery, data: str):
        """Handle search-related callbacks."""
        action = data.replace("search_", "")
        
        if action == "refine":
            await callback_query.message.edit_text(
                f"🔍 {hbold('Refine Search')}\n\n"
                f"Please send me a new search query to refine your results."
            )
        elif action == "new":
            await callback_query.message.edit_text(
                f"🆕 {hbold('New Search')}\n\n"
                f"Send me what you're looking for!"
            )
        else:
            await callback_query.answer("Unknown search action", show_alert=True)
    
    async def _handle_product_callback(self, callback_query: CallbackQuery, data: str):
        """Handle product-related callbacks."""
        product_id = data.replace("product_", "")
        
        # TODO: Fetch actual product details
        await callback_query.message.edit_text(
            f"📦 {hbold('Product Details')}\n\n"
            f"Product ID: {product_id}\n"
            f"🚧 Detailed product view will be implemented soon!"
        )
    
    async def _handle_marketplace_callback(self, callback_query: CallbackQuery, data: str):
        """Handle marketplace-related callbacks."""
        marketplace = data.replace("marketplace_", "")
        
        await callback_query.message.edit_text(
            f"🛒 {hbold(f'{marketplace.title()} Results')}\n\n"
            f"Showing results from {marketplace}\n"
            f"🚧 Marketplace-specific filtering will be implemented soon!"
        )
    
    async def _handle_filter_callback(self, callback_query: CallbackQuery, data: str):
        """Handle filter-related callbacks."""
        filter_type = data.replace("filter_", "")
        
        if filter_type == "price":
            text = f"💰 {hbold('Price Filter')}\n\nSend your price range (e.g., '5000-15000')"
        elif filter_type == "rating":
            text = f"⭐ {hbold('Rating Filter')}\n\nMinimum rating applied!"
        elif filter_type == "availability":
            text = f"✅ {hbold('Availability Filter')}\n\nShowing only available products!"
        else:
            text = f"🔧 {hbold('Filter Applied')}\n\nFilter: {filter_type}"
        
        await callback_query.message.edit_text(text)
    
    async def _handle_unknown_callback(self, callback_query: CallbackQuery, data: str):
        """Handle unknown callback queries."""
        await callback_query.answer(
            f"Unknown action: {data}",
            show_alert=True
        )