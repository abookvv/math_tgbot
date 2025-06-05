from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Dict
from utils.i18n import Translator

class LanguageMiddleware(BaseMiddleware):
    instance = None
    def __init__(self, translator: Translator):
        self.translator = translator
        self.user_lang: Dict[int, str] = {}  # user_id -> lang
        LanguageMiddleware.instance = self

    async def __call__(self, handler, event: TelegramObject, data: dict):
        user_id = event.from_user.id
        lang = self.user_lang.get(user_id, "ru")
        data["t"] = lambda key: self.translator.t(key, lang)
        return await handler(event, data)

    def set_language(self, user_id: int, lang: str):
        self.user_lang[user_id] = lang
