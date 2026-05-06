from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards.support_kb import support_menu
from keyboards.main_kb import main_menu
from services.support_service import create_ticket

router = Router()


class SupportState(StatesGroup):
    waiting_description = State()


@router.message(F.text.in_([
    "📡 Немає інтернету",
    "🐢 Повільна швидкість",
    "📶 Проблема з роутером"
]))
async def start_ticket(message: Message, state: FSMContext):

    problem_map = {
        "📡 Немає інтернету": "no_internet",
        "🐢 Повільна швидкість": "slow_speed",
        "📶 Проблема з роутером": "router_issue"
    }

    await state.update_data(
        problem_type=problem_map.get(message.text)
    )

    await message.answer(
        "✍ Опишіть проблему детально:"
    )

    await state.set_state(SupportState.waiting_description)


@router.message(SupportState.waiting_description)
async def save_description(message: Message, state: FSMContext):

    data = await state.get_data()
    problem_type = data.get("problem_type")

    create_ticket(
        telegram_id=message.from_user.id,
        problem_type=problem_type,
        description=message.text
    )

    await state.clear()

    await message.answer(
        "✅ Заявку створено!\n"
        "Наші техніки вже працюють.",
        reply_markup=main_menu()
    )

@router.message(F.text == "🔙 Назад")
async def back(message: Message, state: FSMContext):

    await state.clear()

    await message.answer(
        "Головне меню:",
        reply_markup=main_menu()
    )

@router.message(F.text == "🛠 Техпідтримка")
async def open_support(message: Message):
    await message.answer(
        "🛠 Оберіть проблему:",
        reply_markup=support_menu()
    )