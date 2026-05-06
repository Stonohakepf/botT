from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="👤 Особистий кабінет"),
                KeyboardButton(text="💳 Оплата інтернету"),
            ],
            [
                KeyboardButton(text="📶 Перевірка інтернету"),
                KeyboardButton(text="🛠 Техпідтримка"),
            ],
            [
                KeyboardButton(text="⚡ Швидкість інтернету"),
                KeyboardButton(text="📦 Тарифи"),
            ],
            [
                KeyboardButton(text="❓ FAQ"),
                KeyboardButton(text="📍 Покриття"),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )