from aiogram import Router

from .add_word.dialog import dialog as add_word_dialog
from .all_words.dialog import dialog as all_words_dialog
from .collections.dialog import dialog as collections_dialog
from .home.dialog import dialog as home_dialog

dialogs_router = Router()

dialogs_router.include_router(home_dialog)
dialogs_router.include_router(all_words_dialog)
dialogs_router.include_router(collections_dialog)
dialogs_router.include_router(add_word_dialog)
