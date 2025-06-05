from aiogram.fsm.state import StatesGroup, State

class ViewQuizStates(StatesGroup):
    choosing_quiz = State()
    choosing_ticket = State()

class StartPrepStates(StatesGroup):
    choosing_quiz = State()
    entering_number = State()
    showing_tickets = State()

class EditQuizStates(StatesGroup):
    choosing_action = State()
    choosing_quiz = State()
    editing = State()
