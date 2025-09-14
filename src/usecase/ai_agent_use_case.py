"""AI Agent use case for handling LLM interactions."""

from typing import List, Optional

from langchain.schema import BaseMessage, HumanMessage, SystemMessage
from loguru import logger

from src.config.config import settings
from src.types.models import AIResponse, User, SearchQuery


class AIAgentUseCase:
    """Use case for AI agent interactions."""
    
    def __init__(self):
        self.model_name = settings.ai.model_name
        self.max_tokens = settings.ai.max_tokens
        self.temperature = settings.ai.temperature
        
        # TODO: Initialize actual LLM when OpenAI key is provided
        self.llm = None
        
    async def process_message(self, user: User, message: str) -> AIResponse:
        """Process user message with AI agent."""
        
        try:
            # Create conversation context
            messages = await self._create_conversation_context(user, message)
            
            # Get AI response
            ai_text = await self._get_ai_response(messages)
            
            # Analyze intent and entities
            intent = await self._analyze_intent(message)
            entities = await self._extract_entities(message)
            suggested_actions = await self._get_suggested_actions(intent, entities)
            
            return AIResponse(
                text=ai_text,
                confidence=0.85,  # Mock confidence score
                intent=intent,
                entities=entities,
                suggested_actions=suggested_actions
            )
            
        except Exception as e:
            logger.error(f"AI processing failed: {str(e)}")
            return AIResponse(
                text="Sorry, I encountered an error processing your request. Please try again.",
                confidence=0.0,
                intent="error",
                entities={},
                suggested_actions=["retry", "help"]
            )
    
    async def generate_search_query(self, user_input: str) -> SearchQuery:
        """Generate structured search query from user input."""
        
        try:
            # Use AI to understand and structure the search query
            intent = await self._analyze_intent(user_input)
            entities = await self._extract_entities(user_input)
            
            # Extract search parameters
            query_text = await self._extract_search_terms(user_input, entities)
            price_range = await self._extract_price_range(user_input, entities)
            
            return SearchQuery(
                user_id=0,  # Will be set by the caller
                query_text=query_text,
                marketplaces=[],  # Will be determined based on user preferences
                max_results=10,
                price_min=price_range.get("min"),
                price_max=price_range.get("max")
            )
            
        except Exception as e:
            logger.error(f"Search query generation failed: {str(e)}")
            # Return basic query as fallback
            return SearchQuery(
                user_id=0,
                query_text=user_input,
                marketplaces=[],
                max_results=10
            )
    
    async def _create_conversation_context(self, user: User, message: str) -> List[BaseMessage]:
        """Create conversation context for AI."""
        
        system_prompt = (
            "You are an AI assistant for an e-commerce search bot. "
            "Help users find products across OZON, Wildberries, and Yandex Market. "
            "Be helpful, concise, and focus on understanding search intent. "
            "If users ask for product searches, guide them to use specific queries."
        )
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"User {user.first_name or 'User'} says: {message}")
        ]
        
        return messages
    
    async def _get_ai_response(self, messages: List[BaseMessage]) -> str:
        """Get response from AI model."""
        
        if not self.llm:
            # Fallback response when AI is not configured
            return (
                "I'm ready to help you search for products! "
                "Just tell me what you're looking for and I'll search across "
                "OZON, Wildberries, and Yandex Market for you."
            )
        
        # TODO: Implement actual LLM call
        # response = await self.llm.agenerate([messages])
        # return response.generations[0][0].text
        
        return "AI response placeholder"
    
    async def _analyze_intent(self, message: str) -> Optional[str]:
        """Analyze user intent from message."""
        
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["найти", "поиск", "ищу", "find", "search"]):
            return "search"
        elif any(word in message_lower for word in ["купить", "заказать", "buy", "order"]):
            return "purchase"
        elif any(word in message_lower for word in ["сравнить", "compare"]):
            return "compare"
        elif any(word in message_lower for word in ["помощь", "help"]):
            return "help"
        else:
            return "general"
    
    async def _extract_entities(self, message: str) -> dict:
        """Extract entities from user message."""
        
        entities = {}
        
        # Simple entity extraction (in real implementation, use NER)
        message_lower = message.lower()
        
        # Product categories
        categories = ["ноутбук", "телефон", "наушники", "laptop", "phone", "headphones"]
        for category in categories:
            if category in message_lower:
                entities["category"] = category
                break
        
        # Brands
        brands = ["apple", "samsung", "sony", "asus", "hp", "эпл", "самсунг"]
        for brand in brands:
            if brand in message_lower:
                entities["brand"] = brand
                break
        
        return entities
    
    async def _get_suggested_actions(self, intent: str, entities: dict) -> List[str]:
        """Get suggested actions based on intent and entities."""
        
        if intent == "search":
            return ["refine_search", "set_filters", "view_results"]
        elif intent == "purchase":
            return ["view_product", "compare_prices", "go_to_store"]
        elif intent == "help":
            return ["show_commands", "search_examples"]
        else:
            return ["search", "help"]
    
    async def _extract_search_terms(self, user_input: str, entities: dict) -> str:
        """Extract clean search terms from user input."""
        
        # Remove common search prefixes
        search_prefixes = ["найти", "поиск", "ищу", "нужен", "find", "search", "looking for"]
        
        clean_input = user_input.lower()
        for prefix in search_prefixes:
            clean_input = clean_input.replace(prefix, "").strip()
        
        return clean_input or user_input
    
    async def _extract_price_range(self, user_input: str, entities: dict) -> dict:
        """Extract price range from user input."""
        
        import re
        
        # Look for price patterns like "до 10000", "от 5000 до 15000", "under 100"
        price_patterns = [
            r"от\s+(\d+)\s+до\s+(\d+)",  # от X до Y
            r"(\d+)\s*-\s*(\d+)",        # X-Y
            r"до\s+(\d+)",               # до X
            r"от\s+(\d+)",               # от X
            r"under\s+(\d+)",            # under X
            r"over\s+(\d+)",             # over X
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, user_input.lower())
            if match:
                groups = match.groups()
                if len(groups) == 2:
                    return {"min": int(groups[0]), "max": int(groups[1])}
                elif "до" in pattern or "under" in pattern:
                    return {"max": int(groups[0])}
                elif "от" in pattern or "over" in pattern:
                    return {"min": int(groups[0])}
        
        return {}