from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from services.database import QuizDB
from keyboards.inline import edit_menu_kb, quizzes_kb
import uuid
from states.edit import EditStates
import logging

router = Router()
db = QuizDB()

# --- Главное меню редактирования ---
@router.message(F.text.func(lambda text: "✏️" in text))
async def edit_quiz_menu(message: Message, state: FSMContext, t):
    await message.answer(t("choose_edit_action"), reply_markup=edit_menu_kb(t))
    await state.set_state(EditStates.choosing_action)
    logging.info(f"User {message.from_user.id} opened edit menu")

# --- Добавление квиза ---
@router.callback_query(F.data == "edit:add_quiz")
async def add_quiz_prompt(callback: CallbackQuery, state: FSMContext, t):
    await callback.message.edit_text(t("enter_quiz_name"))
    await state.set_state(EditStates.waiting_for_quiz_title)
    logging.info(f"User {callback.from_user.id} started quiz creation")

@router.message(EditStates.waiting_for_quiz_title)
async def add_quiz_save(message: Message, state: FSMContext, t):
    quiz_id = str(uuid.uuid4())
    title = message.text
    await db.add_quiz(quiz_id, title)
    await message.answer(t("quiz_created").format(title=title))
    await state.clear()
    logging.info(f"User {message.from_user.id} created quiz '{title}' with ID {quiz_id}")

# --- Удаление квиза ---
@router.callback_query(F.data == "edit:delete_quiz")
async def delete_quiz_choose(callback: CallbackQuery, state: FSMContext, t):
    quizzes = await db.get_quizzes()
    if not quizzes:
        await callback.message.edit_text(t("no_quizzes"))
        return
    await callback.message.edit_text(t("choose_quiz_delete"), reply_markup=quizzes_kb(quizzes, "delete_quiz"))
    await state.set_state(EditStates.choosing_quiz_to_delete)
    logging.info(f"User {callback.from_user.id} chose to delete a quiz")

@router.callback_query(F.data.startswith("delete_quiz:"), EditStates.choosing_quiz_to_delete)
async def delete_quiz_confirm(callback: CallbackQuery, state: FSMContext, t):
    quiz_id = callback.data.split(":")[1]
    await db.delete_quiz_by_id(quiz_id)
    await callback.message.edit_text(t("quiz_deleted"))
    await state.clear()
    print(f"[DEBUG] Deleting quiz with ID: {quiz_id}")
    logging.info(f"User {callback.from_user.id} is deleting quiz with ID {quiz_id}")

# --- Добавление билета ---
@router.callback_query(F.data == "edit:add_ticket")
async def add_ticket_select_quiz(callback: CallbackQuery, state: FSMContext, t):
    quizzes = await db.get_quizzes()
    if not quizzes:
        await callback.message.edit_text(t("no_quizzes"))
        return
    await callback.message.edit_text(t("choose_quiz_add_ticket"), reply_markup=quizzes_kb(quizzes, "add_ticket_quiz"))
    await state.set_state(EditStates.choosing_quiz_to_add_ticket)

@router.callback_query(F.data.startswith("add_ticket_quiz:"), EditStates.choosing_quiz_to_add_ticket)
async def add_ticket_question(callback: CallbackQuery, state: FSMContext, t):
    quiz_id = callback.data.split(":")[1]
    await state.update_data(quiz_id=quiz_id)
    await callback.message.edit_text(t("enter_question"))
    await state.set_state(EditStates.waiting_for_ticket_question)

@router.message(EditStates.waiting_for_ticket_question)
async def add_ticket_answer_prompt(message: Message, state: FSMContext, t):
    await state.update_data(question=message.text)
    await message.answer(t("enter_answer"))
    await state.set_state(EditStates.waiting_for_ticket_answer)

@router.message(EditStates.waiting_for_ticket_answer)
async def save_ticket(message: Message, state: FSMContext, t):
    data = await state.get_data()
    await db.add_ticket(str(uuid.uuid4()), data["quiz_id"], data["question"], message.text)
    await message.answer(t("ticket_created"))
    await state.clear()

# --- Удаление билетов ---
@router.callback_query(F.data == "edit:delete_ticket")
async def delete_ticket_choose_quiz(callback: CallbackQuery, state: FSMContext, t):
    quizzes = await db.get_quizzes()
    if not quizzes:
        await callback.message.edit_text(t("no_quizzes"))
        return
    await callback.message.edit_text(t("choose_quiz_delete_ticket"), reply_markup=quizzes_kb(quizzes, "delete_ticket_quiz"))
    await state.set_state(EditStates.choosing_quiz_to_delete_ticket)

@router.callback_query(F.data.startswith("delete_ticket_quiz:"), EditStates.choosing_quiz_to_delete_ticket)
async def delete_tickets_from_quiz(callback: CallbackQuery, state: FSMContext, t):
    quiz_id = callback.data.split(":")[1]
    await db.delete_tickets_by_quiz_id(quiz_id)
    await callback.message.edit_text(t("tickets_deleted"))
    await state.clear()
    print(f"[DEBUG] Deleting tickets for quiz ID: {quiz_id}")
