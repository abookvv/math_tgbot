from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from services.database import QuizDB

class StorageMiddleware(BaseMiddleware):
    def __init__(self, storage: QuizDB):
        super().__init__()
        self.storage = storage

    async def __call__(self, handler, event: TelegramObject, data: dict):
        data['quiz_storage'] = self.storage
        return await handler(event, data)