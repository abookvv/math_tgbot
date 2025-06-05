from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Кнопки редактирования квиза
def edit_menu_kb(t):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t("add_quiz"), callback_data="edit:add_quiz")],
        [InlineKeyboardButton(text=t("delete_quiz"), callback_data="edit:delete_quiz")],
        [InlineKeyboardButton(text=t("add_ticket"), callback_data="edit:add_ticket")],
        [InlineKeyboardButton(text=t("delete_ticket"), callback_data="edit:delete_ticket")]
    ])

# Выбор квиза по его названию (для удаления или добавления билета)
def quizzes_kb(quizzes: list[tuple[str, str]], prefix: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=title, callback_data=f"{prefix}:{quiz_id}")]
            for quiz_id, title in quizzes
        ]
    )

# Кнопка "Далее" для тренировки (приходит рандомный билет)
def next_ticket_kb(t) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t("next_ticket"), callback_data="prep:next")]
        ]
    )

# Клавиатура выбора языка
def language_kb(t) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en")]
    ])
