from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_kb(t) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t("menu_view"))],
            [KeyboardButton(text=t("menu_prep"))],
            [KeyboardButton(text=t("menu_edit"))],
            [KeyboardButton(text=t("menu_wolfram"))],
        ],
        resize_keyboard=True,
        input_field_placeholder=t("choose_action")
    )
