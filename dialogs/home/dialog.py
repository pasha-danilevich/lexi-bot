from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Row, Start
from aiogram_dialog.widgets.text import Const, Format

from . import event_handler, getters
from .state import Home

dialog = Dialog(
    Window(
        Const("Привет!"),
        Format("Всего слов: {total_words}"),
        Row(
            Start(Const("Все слова"), state=..., id='all_words'),
            Start(Const("Статистика"), state=..., id='statistic'),
        ),
        Start(Const("Повторять"), state=..., id='training'),
        Start(Const("Добавить новое слово"), state=..., id='add_new_word'),
        getter=getters.get_msg,
        state=Home.home,
    ),
    on_start=event_handler.on_start,
)
