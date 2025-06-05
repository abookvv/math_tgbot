from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
import logging
from keyboards import inline
# from keyboards.inline import main_menu
from keyboards.builders import main_menu_kb
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from middlewares.language_middleware import LanguageMiddleware

from routers.handlers import view_quiz, edit_quiz, start_prep, wolfram

router = Router()

@router.message(F.text.in_({"/start", "/menu"}))
async def start_command(message: Message, t):
    await message.answer(
        t("welcome_message"),
        reply_markup=main_menu_kb(t)
    )
    logging.info(f"User {message.from_user.id} called /start")

@router.message(Command("help"))
async def help_command(message: Message, t):
    await message.answer(
        t("help_message")
    )

@router.message(Command("tellabout"))
async def help_command(message: Message, t):
    await message.answer(
        t("tellabout_message")
    )

@router.message(Command("author"))
async def help_command(message: Message, t):
    await message.answer(
        t("author_message")
    )

# Обработка кнопки "📚 Посмотреть квиз"
@router.message(F.text.func(lambda text: "📚" in text))
async def route_to_view_quiz(message: Message, state, t):
    return await view_quiz.view_quiz_start(message, state, t)

# "🎯 Начать подготовку"
@router.message(F.text.func(lambda text: "🎯" in text))
async def route_to_start_prep(message: Message, state, t):
    return await start_prep.start_prep(message, state, t)

# "✏️ Редактировать квиз"
@router.message(F.text.func(lambda text: "✏️" in text))
async def route_to_edit_quiz(message: Message, state, t):
    return await edit_quiz.edit_quiz_menu(message, state, t)

# "🧠 Вольфрам" — объяснение
@router.message(F.text.func(lambda text: "🧠" in text))
async def wolfram_entry(message: Message, t):
    return await wolfram.wolfram_intro(message, t)

# Обработка произвольного запроса к WolframAlpha
@router.message(F.text.startswith("W:"))  # Пользователь пишет "W:integrate x^2"
async def wolfram_query(message: Message, t):
    return await wolfram.handle_wolfram_query(message, t)


language_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru")],
    [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en")]
])

@router.message(Command("language"))
async def change_language(message: Message, t):
    await message.answer(t("choose_language"), reply_markup=language_kb)

@router.callback_query(F.data.startswith("lang:"))
async def set_lang(callback: CallbackQuery):
    lang = callback.data.split(":")[1]
    user_id = callback.from_user.id

    # Получаем language_middleware вручную (если нужно)
    language_middleware = LanguageMiddleware.instance  # или аналог, если ты его сохраняешь где-то
    language_middleware.set_language(user_id, lang)

    msg = "✅ Language changed!" if lang == "en" else "✅ Язык изменён!"
    await callback.message.edit_text(msg)