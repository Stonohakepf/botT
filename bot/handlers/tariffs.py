from aiogram import Router, F
from aiogram.types import Message

from keyboards.main_kb import main_menu
from database.queries import (
    create_user_if_not_exists,
    get_user,
    update_tariff,
    get_balance,
    update_balance
)

router = Router()


TARIFFS = {
    "Basic": {"speed": "50 Mbps", "price": 100},
    "Standard": {"speed": "100 Mbps", "price": 150},
    "Pro": {"speed": "300 Mbps", "price": 250},
}


@router.message(F.text == "📦 Тарифи")
async def show_tariffs(message: Message):

    create_user_if_not_exists(message.from_user.id)
    user = get_user(message.from_user.id)

    current_tariff = user[2]
    balance = user[1]

    text = (
        "📦 <b>Доступні тарифи</b>\n\n"
        f"💳 Ваш баланс: <b>{balance} грн</b>\n"
        f"📌 Поточний тариф: <b>{current_tariff}</b>\n\n"
    )

    for name, data in TARIFFS.items():
        mark = "👈 поточний" if name == current_tariff else ""
        text += (
            f"📶 <b>{name}</b> {mark}\n"
            f"⚡ Швидкість: {data['speed']}\n"
            f"💰 Ціна: {data['price']} грн/міс\n\n"
        )

    text += "👉 Напишіть назву тарифу для зміни"

    await message.answer(text, parse_mode="HTML")


@router.message(F.text.in_(["Basic", "Standard", "Pro"]))
async def change_tariff(message: Message):

    telegram_id = message.from_user.id
    new_tariff = message.text

    create_user_if_not_exists(telegram_id)
    user = get_user(telegram_id)

    current_tariff = user[2]
    balance = user[1]

    price = TARIFFS[new_tariff]["price"]

    if new_tariff == current_tariff:
        await message.answer(
            f"ℹ️ Ви вже на тарифі <b>{new_tariff}</b>",
            parse_mode="HTML",
            reply_markup=main_menu()
        )
        return

    if balance < price:
        await message.answer(
            f"❌ Недостатньо коштів!\n"
            f"💰 Потрібно: {price} грн\n"
            f"💳 Ваш баланс: {balance} грн",
            parse_mode="HTML",
            reply_markup=main_menu()
        )
        return

    new_balance = balance - price

    update_tariff(telegram_id, new_tariff)
    update_balance(telegram_id, new_balance)

    await message.answer(
        f"✅ Тариф змінено на <b>{new_tariff}</b>\n"
        f"💰 Списано: {price} грн\n"
        f"💳 Новий баланс: {new_balance} грн\n\n"
        f"📶 Швидкість: {TARIFFS[new_tariff]['speed']}",
        parse_mode="HTML",
        reply_markup=main_menu()
    )