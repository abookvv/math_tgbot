from aiogram.fsm.state import StatesGroup, State

class ViewQuiz(StatesGroup):
    selecting_quiz = State()
    selecting_ticket = State()
