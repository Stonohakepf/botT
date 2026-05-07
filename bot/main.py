import os
import asyncio
from aiohttp import web

from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from bot.config import BOT_TOKEN
from database.models import create_tables

from bot.handlers import (
    menu,
    profile,
    payments,
    support,
    tariffs,
    speedtest,
    faq,
    coverage,
    custom_payment
)

WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = "secret123"

BASE_WEBHOOK_URL = os.getenv("BASE_WEBHOOK_URL")


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def register_routers():
    dp.include_router(menu.router)
    dp.include_router(profile.router)
    dp.include_router(payments.router)
    dp.include_router(support.router)
    dp.include_router(speedtest.router)
    dp.include_router(tariffs.router)
    dp.include_router(coverage.router)
    dp.include_router(faq.router)
    dp.include_router(custom_payment.router)


async def on_startup(bot: Bot):
    create_tables()

    await bot.set_webhook(
        url=f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}",
        secret_token=WEBHOOK_SECRET
    )

    print("Webhook set")


async def on_shutdown(bot: Bot):
    await bot.delete_webhook()


async def main():
    register_routers()

    app = web.Application()

    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET
    ).register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    app.on_startup.append(lambda _: on_startup(bot))
    app.on_shutdown.append(lambda _: on_shutdown(bot))

    port = int(os.getenv("PORT", 10000))

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, host="0.0.0.0", port=port)
    await site.start()

    print(f"Bot started on port {port}")

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
