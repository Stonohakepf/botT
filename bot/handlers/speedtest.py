from aiogram import Router, F
from aiogram.types import Message

from services.speed_service import run_speedtest

router = Router()


@router.message(F.text == "⚡ Швидкість інтернету")
async def speedtest_handler(message: Message):

    msg = await message.answer("⚡ Виконуємо speedtest... почекай 10–20 сек")

    result = run_speedtest()

    await msg.edit_text(
        f"⚡ <b>Результати Speedtest</b>\n\n"
        f"📥 Download: <b>{result['download']} Mbps</b>\n"
        f"📤 Upload: <b>{result['upload']} Mbps</b>\n"
        f"📶 Ping: <b>{result['ping']} ms</b>",
        parse_mode="HTML"
    )