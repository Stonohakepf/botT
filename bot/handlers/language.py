from aiogram import Router, F
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database.db import get_connection

router = Router()


def lang_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇺🇦 Українська")],
            [KeyboardButton(text="🇬🇧 English")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )


@router.message(F.text == "🌐 Мова")
async def open_lang_menu(message: Message):
    await message.answer("🌐 Оберіть мову:", reply_markup=lang_menu())


@router.message(F.text.in_(["🇺🇦 Українська", "🇬🇧 English"]))
async def set_lang(message: Message):

    lang = "uk" if "Українська" in message.text else "en"

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET language = ? WHERE telegram_id = ?",
        (lang, message.from_user.id)
    )

    conn.commit()
    conn.close()

    await message.answer("✅ Мову змінено")


@router.message(F.text == "🔙 Назад")
async def back(message: Message):
    from keyboards.main_kb import main_menu

    await message.answer("Головне меню:", reply_markup=main_menu())