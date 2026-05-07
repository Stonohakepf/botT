from aiogram import Router, F
from aiogram.types import Message
from keyboards.main_kb import main_menu
from keyboards.faq_kb import faq_kb
router = Router()


FAQ_DATA = {
    "❓ Як оплатити?": "💳 Через меню 'Оплата інтернету'",
    "🐢 Чому повільний інтернет?": "⚠️ Може бути перевантаження або тариф",
    "🔌 Як перезавантажити роутер?": "Вимкніть на 10 сек",
    "📡 Чому немає інтернету?": "Перевірте баланс або аварію"
}


@router.message(F.text == "❓ FAQ")
async def faq_menu(message: Message):
    await message.answer(
        "❓ Оберіть питання:",
        reply_markup=faq_kb()
    )

@router.message(F.text.in_(FAQ_DATA.keys()))
async def faq_answer(message: Message):
    await message.answer(FAQ_DATA[message.text])


@router.message(F.text == "⬅️ Назад")
async def back_to_menu(message: Message):
    await message.answer("Головне меню:", reply_markup=main_menu())