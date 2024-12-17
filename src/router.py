# src/router.py

from aiogram import Router

from handlers.my_profile import router as my_profile_router
from handlers.start import router as start_router

main_router = Router()

# Регистрация маршрутов из других модулей

main_router.include_router(my_profile_router)
main_router.include_router(start_router)
