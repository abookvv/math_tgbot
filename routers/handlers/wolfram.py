from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from services.wolfram_queries import WolframClient

router = Router()
wolfram_client  = WolframClient()

async def wolfram_intro(message: Message, t):
    await message.answer(t("wolfram_intro"))

async def handle_wolfram_query(message: Message, t):
    query = message.text.strip().removeprefix("W:").strip()
    result = await wolfram_client.ask(query)
    await message.answer(result or t("wolfram_no_result"))