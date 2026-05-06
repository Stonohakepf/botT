from aiogram import Router, F
from aiogram.types import Message

from database.queries import get_or_create_user

router = Router()

@router.message(F.text == "👤 Особистий кабінет")
async def profile(message: Message):
    user = get_or_create_user(message.from_user.id)

    text = (
        "👤 <b>Особистий кабінет</b>\n\n"
        f"💰 Баланс: <b>{user[2]} грн</b>\n"
        f"📦 Тариф: <b>{user[3]}</b>\n"
        f"📶 Статус: <b>{user[4]}</b>\n"
        f"📅 Наступна оплата: <b>{user[5]}</b>\n"
    )

    await message.answer(text, parse_mode="HTML")