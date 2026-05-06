import asyncio
from aiogram import Bot, Dispatcher
from bot.config import BOT_TOKEN
from database.models import create_tables
from bot.handlers import menu, profile, payments, support, tariffs, speedtest, faq, coverage, language, custom_payment

async def main():
    create_tables()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(menu.router)
    dp.include_router(profile.router)
    dp.include_router(payments.router)
    dp.include_router(support.router)
    dp.include_router(speedtest.router)
    dp.include_router(tariffs.router)
    dp.include_router(coverage.router)
    dp.include_router(faq.router)
    dp.include_router(language.router)
    dp.include_router(custom_payment.router)
    

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())