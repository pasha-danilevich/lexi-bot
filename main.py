import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs
from aiogram_dialog.context.media_storage import MediaIdStorage
from aiogram_dialog.manager.message_manager import MessageManager
from loguru import logger

from bot.dialog_manager.factory import ManagerFactory
from bot.dialogs import dialogs_router
from bot.handlers import main_router
from bot.middlewares.register import register_middlewares
from config import config
from db.database import init_db


# Запуск бота
async def main():
    await init_db()
    bot = Bot(token=config.BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    register_middlewares(dp)

    dp.include_routers(main_router)
    dp.include_routers(dialogs_router)

    setup_dialogs(
        dp,
        dialog_manager_factory=ManagerFactory(
            message_manager=MessageManager(),
            media_id_storage=MediaIdStorage(),
        ),
    )
    logger.success('Бот запущен!')
    await bot.send_message(chat_id=850472798, text='Я запустился /start')

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
