from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from states.state import StartPrepStates
from services.database import QuizDB
import random
from utils.escape_md_re import escape_markdown

router = Router()
quiz_db = QuizDB()

@router.message(F.text.func(lambda text: "🎯" in text))
async def start_prep(message: Message, state: FSMContext, t):
    quizzes = await quiz_db.get_quizzes()
    if not quizzes:
        await message.answer(t("no_quizzes"))
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=titles, callback_data=f"prep_quiz:{q}")]
        for q, titles in quizzes
    ])

    await message.answer(t("choose_quiz"), reply_markup=kb)
    await state.set_state(StartPrepStates.choosing_quiz)

@router.callback_query(F.data.startswith("prep_quiz:"), StartPrepStates.choosing_quiz)
async def input_count(callback: CallbackQuery, state: FSMContext, t):
    quiz = callback.data.split(":")[1]
    await state.update_data(quiz=quiz)
    await callback.message.edit_text(t("enter_ticket_count"))
    await state.set_state(StartPrepStates.entering_number)

@router.message(StartPrepStates.entering_number)
async def collect_tickets(message: Message, state: FSMContext, t):
    if not message.text.isdigit():
        await message.answer(t("please_enter_number"))
        return

    count = int(message.text)
    data = await state.get_data()
    quiz = data["quiz"]
    all_tickets = await quiz_db.get_tickets(quiz)
    if not all_tickets:
        await message.answer(t("no_tickets"))
        await state.clear()
        return

    selected = random.sample(all_tickets, min(count, len(all_tickets)))
    await state.update_data(tickets=selected, index=0)
    await show_next_ticket(message, state, t)

@router.callback_query(F.data == "prep_next_ticket", StartPrepStates.showing_tickets)
async def next_ticket(callback: CallbackQuery, state: FSMContext, t):
    await show_next_ticket(callback.message, state, t)

async def show_next_ticket(message: Message, state: FSMContext, t):
    data = await state.get_data()
    tickets = data["tickets"]
    index = data["index"]
    quiz = data["quiz"]

    if index >= len(tickets):
        await message.answer(t("no_more_tickets"))
        await state.clear()
        return

    print(tickets)
    # ticket_id = tickets[index]
    # ticket = await quiz_db.get_ticket_by_id(quiz, ticket_id)
    ticket = tickets[index]
    print(ticket)

    text = (
        f"{escape_markdown(t('ticket'))} {index + 1}:\n\n"
        f"{escape_markdown(t('question'))}:\n{escape_markdown(ticket['question'])}\n\n"
        f"{escape_markdown(t('answer'))}:\n||{escape_markdown(ticket.get('answer', t('no_answer')))}||"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t("next"), callback_data="prep_next_ticket")]
    ])

    await message.answer(text, reply_markup=kb, parse_mode="MarkdownV2")
    await state.update_data(index=index+1)
    await state.set_state(StartPrepStates.showing_tickets)
