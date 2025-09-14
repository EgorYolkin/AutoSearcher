"""Data models for the AI-agent telegram bot."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class UserRole(str, Enum):
    """User role enumeration."""
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"


class SearchStatus(str, Enum):
    """Search status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class MarketPlace(str, Enum):
    """Marketplace enumeration."""
    OZON = "ozon"
    WILDBERRIES = "wildberries"
    YANDEX_MARKET = "yandex_market"


class User(BaseModel):
    """User model."""
    
    id: int = Field(..., description="Telegram user ID")
    username: Optional[str] = Field(None, description="Telegram username")
    first_name: Optional[str] = Field(None, description="User first name")
    last_name: Optional[str] = Field(None, description="User last name")
    role: UserRole = Field(UserRole.USER, description="User role")
    is_active: bool = Field(True, description="User activity status")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class Product(BaseModel):
    """Product model."""
    
    id: Optional[str] = Field(None, description="Product ID")
    name: str = Field(..., description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    price: Optional[float] = Field(None, description="Product price")
    currency: str = Field("RUB", description="Price currency")
    url: Optional[str] = Field(None, description="Product URL")
    image_url: Optional[str] = Field(None, description="Product image URL")
    marketplace: MarketPlace = Field(..., description="Marketplace")
    rating: Optional[float] = Field(None, description="Product rating")
    reviews_count: Optional[int] = Field(None, description="Number of reviews")
    availability: bool = Field(True, description="Product availability")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class SearchQuery(BaseModel):
    """Search query model."""
    
    id: Optional[str] = Field(None, description="Query ID")
    user_id: int = Field(..., description="User ID who made the query")
    query_text: str = Field(..., description="Search query text")
    marketplaces: List[MarketPlace] = Field(..., description="Target marketplaces")
    max_results: int = Field(10, description="Maximum number of results")
    price_min: Optional[float] = Field(None, description="Minimum price filter")
    price_max: Optional[float] = Field(None, description="Maximum price filter")
    status: SearchStatus = Field(SearchStatus.PENDING, description="Search status")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    completed_at: Optional[datetime] = Field(None, description="Completion timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class SearchResult(BaseModel):
    """Search result model."""
    
    id: Optional[str] = Field(None, description="Result ID")
    query_id: str = Field(..., description="Search query ID")
    products: List[Product] = Field(default_factory=list, description="Found products")
    total_found: int = Field(0, description="Total products found")
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


@dataclass
class BotContext:
    """Bot context for handlers."""
    user: User
    chat_id: int
    message_id: Optional[int] = None
    callback_data: Optional[str] = None
    command: Optional[str] = None
    text: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class AIResponse:
    """AI response model."""
    text: str
    confidence: float = 0.0
    intent: Optional[str] = None
    entities: Dict[str, Any] = None
    suggested_actions: List[str] = None
    
    def __post_init__(self):
        if self.entities is None:
            self.entities = {}
        if self.suggested_actions is None:
            self.suggested_actions = []