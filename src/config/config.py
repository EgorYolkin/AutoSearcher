"""Configuration management for the AI-agent telegram bot."""

import os
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class BotConfig(BaseSettings):
    """Bot configuration settings."""
    
    token: str = Field(..., env="BOT_TOKEN", description="Telegram bot token")
    admin_ids: list[int] = Field(default_factory=list, env="ADMIN_IDS", description="Admin user IDs")
    webhook_url: Optional[str] = Field(None, env="WEBHOOK_URL", description="Webhook URL for production")
    webhook_path: str = Field("/webhook", env="WEBHOOK_PATH", description="Webhook path")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class AIConfig(BaseSettings):
    """AI/LLM configuration settings."""
    
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY", description="OpenAI API key")
    model_name: str = Field("gpt-3.5-turbo", env="MODEL_NAME", description="LLM model name")
    max_tokens: int = Field(1000, env="MAX_TOKENS", description="Maximum tokens for AI responses")
    temperature: float = Field(0.7, env="TEMPERATURE", description="AI response temperature")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class DatabaseConfig(BaseSettings):
    """Database configuration settings."""
    
    database_url: str = Field("sqlite:///./database.db", env="DATABASE_URL", description="Database URL")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class AppConfig(BaseSettings):
    """Application configuration settings."""
    
    debug: bool = Field(False, env="DEBUG", description="Debug mode")
    log_level: str = Field("INFO", env="LOG_LEVEL", description="Logging level")
    host: str = Field("0.0.0.0", env="HOST", description="Application host")
    port: int = Field(8000, env="PORT", description="Application port")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class Settings:
    """Main settings container."""
    
    def __init__(self):
        self.bot = BotConfig()
        self.ai = AIConfig()
        self.database = DatabaseConfig()
        self.app = AppConfig()


# Global settings instance
settings = Settings()