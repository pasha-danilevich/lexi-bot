from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Row, Start
from aiogram_dialog.widgets.text import Const, Format

from ..add_word.state import AddWordSG
from ..all_words.state import AllWordSG
from . import event_handler, getters
from .state import HomeSG

dialog = Dialog(
    Window(
        Const("Привет!"),
        Format("Всего слов: {total_words}"),
        Row(
            Start(Const("Все слова"), state=AllWordSG.all_words, id='all_words'),
            Start(Const("Статистика"), state=..., id='statistic'),
        ),
        Start(Const("Повторять"), state=..., id='training'),
        Start(
            Const("Добавить новое слово"), state=AddWordSG.add_word, id='add_new_word'
        ),
        getter=getters.get_msg,
        state=HomeSG.home,
    ),
    on_start=event_handler.on_start,
)
