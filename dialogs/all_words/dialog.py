from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format

from . import event_handler, getters
from .state import AllWords

dialog = Dialog(
    Window(
        Const("Все слова:"),
        Format("{word_list}"),
        getter=getters.get_msg,
        state=AllWords.all_words,
    ),
    on_start=event_handler.on_start,
)
