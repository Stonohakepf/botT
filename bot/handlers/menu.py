from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from keyboards.main_kb import main_menu

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Вітаю в РО-НЕТ боті.\nОберіть дію:",
        reply_markup=main_menu()
    )