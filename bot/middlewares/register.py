from aiogram import Dispatcher

from bot.middlewares.callback_logger import CallbackLoggerMiddleware


def register_middlewares(dp: Dispatcher):
    dp.callback_query.outer_middleware(CallbackLoggerMiddleware())
