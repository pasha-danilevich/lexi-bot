# src/main.py

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import config
from database import Database
from middleware import CounterMiddleware
from router import main_router


db = Database()


async def main():
    bot = Bot(
        token=config.TG_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(main_router)
    # Установка middleware
    dp.message.middleware(CounterMiddleware())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO)
    print("Бот запущен!")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот отключен.")
        db.close()

    db.close()
