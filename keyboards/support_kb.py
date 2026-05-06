from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def support_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📡 Немає інтернету")],
            [KeyboardButton(text="🐢 Повільна швидкість")],
            [KeyboardButton(text="📶 Проблема з роутером")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )