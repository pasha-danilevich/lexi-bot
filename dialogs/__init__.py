from aiogram import Router

from .all_words.dialog import dialog as all_words_dialog
from .home.dialog import dialog as home_dialog

dialogs_router = Router()

dialogs_router.include_router(home_dialog)
dialogs_router.include_router(all_words_dialog)
