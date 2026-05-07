from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from services.mono_payment import create_mono_invoice
from services.payment_service import confirm_payment

from keyboards.main_kb import main_menu

router = Router()


class PaymentState(StatesGroup):
    waiting_amount = State()
    waiting_confirm = State()


@router.message(F.text == "💰 Ввести сума")
async def ask_amount(message: Message, state: FSMContext):

    await state.set_state(PaymentState.waiting_amount)
    await message.answer("💰 Введіть суму:")


@router.message(PaymentState.waiting_amount)
async def process_amount(message: Message, state: FSMContext):

    if not message.text.isdigit():
        await message.answer("❌ Тільки число")
        return

    amount = int(message.text)

    invoice = create_mono_invoice(amount, message.from_user.id)

    if not invoice["ok"]:
        await message.answer("❌ Помилка Mono API")
        return

    await state.update_data(
        amount=amount,
        invoice_id=invoice["invoice_id"]
    )

    await state.set_state(PaymentState.waiting_confirm)

    await message.answer(
        f"💳 Рахунок створено\n"
        f"💰 {amount} грн\n\n"
        f"🔗 {invoice['pay_url']}\n\n"
        f"👉 Після оплати натисніть: '✅ Я оплатив'"
    )



@router.message(F.text == "✅ Я оплатив")
async def confirm_user_payment(message: Message, state: FSMContext):

    data = await state.get_data()
    amount = data.get("amount")

    if not amount:
        await message.answer("❌ Дані не знайдено")
        return

    confirm_payment(message.from_user.id, amount)

    await state.clear()

    await message.answer("✅ Оплату підтверджено", reply_markup=main_menu())