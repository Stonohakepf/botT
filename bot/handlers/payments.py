from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from services.mono_payment import create_mono_invoice
from services.payment_service import confirm_payment

from keyboards.main_kb import main_menu
from keyboards.payment_kb import payment_menu

router = Router()

class PaymentState(StatesGroup):
    waiting_amount = State()
    waiting_confirm = State()

@router.message(F.text == "💳 Оплата інтернету")
async def open_payments(message: Message):
    await message.answer("💳 Меню оплати:", reply_markup=payment_menu())

@router.message(F.text == "💳 Швидка оплата ( 500 грн )")
async def fast_pay(message: Message, state: FSMContext):

    amount = 500

    invoice = create_mono_invoice(amount, message.from_user.id)

    if not invoice["ok"]:
        await message.answer("❌ Помилка Mono API")
        return

    await message.answer(
        f"⚡ ШВИДКА ОПЛАТА\n\n"
        f"💰 Сума: {amount} грн\n\n"
        f"🔗 {invoice['pay_url']}\n\n"
        f"👉 Після оплати натисніть: '✅ Я оплатив'"
    )

    await state.update_data(amount=amount, invoice_id=invoice["invoice_id"])
    await state.set_state(PaymentState.waiting_confirm)