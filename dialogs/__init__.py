from aiogram import Router

from .home.dialog import dialog as home_dialog


dialogs_router = Router()



dialogs_router.include_router(home_dialog)

