from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def payment_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💳 Швидка оплата ( 500 грн )")],
            [KeyboardButton(text="💰 Ввести суму")],
            [KeyboardButton(text="✅ Я оплатив")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )