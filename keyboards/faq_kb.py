from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def faq_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❓ Як оплатити?")],
            [KeyboardButton(text="🐢 Чому повільний інтернет?")],
            [KeyboardButton(text="🔌 Як перезавантажити роутер?")],
            [KeyboardButton(text="📡 Чому немає інтернету?")],
            [KeyboardButton(text="⬅️ Назад")]
        ],
        resize_keyboard=True
    )