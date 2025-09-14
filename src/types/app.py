"""Application-specific types and type aliases."""

from typing import Any, Callable, Dict, Union

from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, Update

# Type aliases for common aiogram types
MessageHandler = Callable[[Message], Any]
CallbackHandler = Callable[[CallbackQuery], Any]
UpdateHandler = Callable[[Update], Any]

# Bot and dispatcher types
BotInstance = Bot
DispatcherInstance = Dispatcher

# Generic types
JSONDict = Dict[str, Any]
JSONValue = Union[str, int, float, bool, None, Dict[str, Any], list]

# Handler result types
HandlerResult = Union[str, None, Dict[str, Any]]

# AI types
AIPrompt = str
AICompletion = str

__all__ = [
    "MessageHandler",
    "CallbackHandler", 
    "UpdateHandler",
    "BotInstance",
    "DispatcherInstance",
    "JSONDict",
    "JSONValue",
    "HandlerResult",
    "AIPrompt",
    "AICompletion",
]