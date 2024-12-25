# src/router.py

from aiogram import Router

from handlers.my_profile import router as my_profile_router
from handlers.start import router as start_router
from handlers.add_word import router as add_word_router
from handlers.training import router as training_router
from handlers.add_word_to_dict import router as add_word_to_dict_router
from handlers.delete import router as delete_router
from handlers.reproduce import router as reproduce_router

main_router = Router()

# Регистрация маршрутов из других модулей

main_router.include_router(my_profile_router)
main_router.include_router(start_router)
main_router.include_router(add_word_router)
main_router.include_router(training_router)
main_router.include_router(add_word_to_dict_router)
main_router.include_router(delete_router)
main_router.include_router(reproduce_router)
