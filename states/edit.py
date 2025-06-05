# from aiogram.fsm.state import StatesGroup, State
#
# class EditStates(StatesGroup):
#     waiting_for_quiz_title = State()
#     choosing_quiz_to_delete = State()
#     choosing_quiz_to_add_ticket = State()
#     waiting_for_ticket_question = State()
#     waiting_for_ticket_answer = State()
#     choosing_quiz_to_delete_ticket = State()
#     choosing_ticket_to_delete = State()
#     choosing_action = State()
#     choosing_quiz = State()
#     editing = State()
#
#     choosing_action = State()
#     choosing_quiz = State()
#     editing = State()
#
#     adding_quiz = State()
#     deleting_quiz = State()
#     adding_ticket = State()
#     deleting_ticket = State()

from aiogram.fsm.state import StatesGroup, State


class EditStates(StatesGroup):
    # Добавление квиза
    waiting_for_quiz_title = State()

    # Удаление квиза
    choosing_quiz_to_delete = State()

    # Добавление билета в квиз
    choosing_quiz_to_add_ticket = State()
    waiting_for_ticket_question = State()
    waiting_for_ticket_answer = State()

    # Удаление билета из квиза
    choosing_quiz_to_delete_ticket = State()
    choosing_ticket_to_delete = State()

    # Редактирование
    choosing_action = State()  # Добавляем нужное состояние

