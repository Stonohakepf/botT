from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from services.coverage_service import check_internet_status
from services.coverage_service import check_coverage
from keyboards.main_kb import main_menu


router = Router()

class CoverageState(StatesGroup):
    waiting_address = State()


@router.message(F.text == "📍 Покриття")
async def ask_address(message: Message, state: FSMContext):
    await message.answer("📍 Введіть вашу адресу:")
    await state.set_state(CoverageState.waiting_address)


@router.message(CoverageState.waiting_address)
async def process_address(message: Message, state: FSMContext):

    result = check_coverage(message.text)

    if result:
        await message.answer("🟢 У вашій зоні є покриття!")
    else:
        await message.answer("🔴 Покриття відсутнє.")

    await state.clear()

    await message.answer("Головне меню:", reply_markup=main_menu())

@router.message(F.text == "📶 Перевірка інтернету")
async def internet_status_handler(message: Message):

    result = check_internet_status(message.from_user.id)

    await message.answer(
        f"📶 <b>Статус інтернету</b>\n\n{result['message']}",
        parse_mode="HTML"
    )