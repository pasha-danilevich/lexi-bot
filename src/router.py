# src/router.py

from aiogram import Router

from handlers.welcome import router as welcome_router
from handlers.start import router as start_router

main_router = Router()

# Регистрация маршрутов из других модулей

main_router.include_router(welcome_router)
main_router.include_router(start_router)
