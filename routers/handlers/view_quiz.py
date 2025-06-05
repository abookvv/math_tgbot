from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from states.state import ViewQuizStates
from services.database import QuizDB
from utils.escape_md_re import escape_markdown


router = Router()
quiz_db = QuizDB()

@router.message(F.text.func(lambda text: "📚" in text))
async def view_quiz_start(message: Message, state: FSMContext, t):
    quizzes = await quiz_db.get_quizzes()
    if not quizzes:
        await message.answer(t("no_quizzes"))
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=titles, callback_data=f"view_quiz:{q}")]
        for q, titles in quizzes
    ])
    await message.answer(t("choose_quiz"), reply_markup=kb)
    await state.set_state(ViewQuizStates.choosing_quiz)

@router.callback_query(F.data.startswith("view_quiz:"), ViewQuizStates.choosing_quiz)
async def choose_quiz(callback: CallbackQuery, state: FSMContext, t):
    quiz_name = callback.data.split(":")[1]
    tickets = await quiz_db.get_tickets(quiz_name)
    if not tickets:
        await callback.message.edit_text(t("no_tickets"))
        return

    await state.update_data(quiz=quiz_name)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"{ticket['question']}", callback_data=f"view_ticket:{ticket['id']}")]
        for ticket in tickets
    ])
    await callback.message.edit_text(t("choose_ticket"), reply_markup=kb)
    await state.set_state(ViewQuizStates.choosing_ticket)

@router.callback_query(F.data.startswith("view_ticket:"), ViewQuizStates.choosing_ticket)
async def show_ticket(callback: CallbackQuery, state: FSMContext, t):
    data = await state.get_data()
    quiz_name = data["quiz"]
    ticket_id = callback.data.split(":")[1]

    ticket = await quiz_db.get_ticket_by_id(quiz_name, ticket_id)
    if not ticket:
        await callback.message.edit_text(t("ticket_not_found"))
        return

    question = escape_markdown(ticket['question'])
    answer = escape_markdown(ticket.get('answer', t('no_answer')))

    text = f"{t('question')}:\n{question}\n\n{t('answer')}:\n||{answer}||"
    #text = f"{t('question')}:\n{ticket['question']}\n\n{t('answer')}:\n||{ticket.get('answer', t('no_answer'))}||"
    await callback.message.edit_text(text, parse_mode="MarkdownV2")
    await state.clear()
