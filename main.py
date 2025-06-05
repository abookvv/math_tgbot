from config.settings_bot import bot_config
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import logging
import asyncio

from routers import commands
from routers.handlers import edit_quiz, start_prep, view_quiz, wolfram

from utils.logger import get_logger
from services.database import QuizDB
from utils.i18n import Translator
from middlewares.language_middleware import LanguageMiddleware
from middlewares.storage_middleware import StorageMiddleware

logger = get_logger()

translator = Translator()
language_middleware = LanguageMiddleware(translator)
LanguageMiddleware.instance = language_middleware

async def main():
    bot = Bot(token=bot_config.telegram_api_key)
    quiz_db  = QuizDB("storage/database.db")
    await quiz_db.init()
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Регистрация роутеров
    dp.include_router(commands.router)
    dp.include_router(view_quiz.router)
    dp.include_router(start_prep.router)
    dp.include_router(edit_quiz.router)
    dp.include_router(wolfram.router)

    #Middleware
    dp.message.middleware(StorageMiddleware(quiz_db ))
    dp.message.middleware(language_middleware)
    dp.callback_query.middleware(language_middleware)

    print("Bot is running...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.info("Starting bot...")
    asyncio.run(main())


