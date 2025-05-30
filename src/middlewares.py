from pyexpat.errors import messages

from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Dict, Any, Awaitable, Callable

from settings.config import ADMIN_IDS


class BotMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.is_admin = False

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        self.is_admin = True if str(event.from_user.id) in ADMIN_IDS else False
        data['is_admin'] = self.is_admin
        return await handler(event, data)
