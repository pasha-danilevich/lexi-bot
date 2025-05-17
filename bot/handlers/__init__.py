from aiogram import Router

from .commands import router

main_router = Router()

main_router.include_router(router)
