from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Back, Button, Row, SwitchTo
from aiogram_dialog.widgets.text import Const, Format

from ..common import buttons
from . import event_handler, getters
from .state import AllWordSG

dialog = Dialog(
    Window(
        Const("Все слова:"),
        Format("{word_list}"),
        Row(
            buttons.HOME,
            SwitchTo(
                Const('Найти слово'), state=AllWordSG.search_word, id='search_word'
            ),
        ),
        getter=getters.get_msg,
        state=AllWordSG.all_words,
    ),
    Window(
        Const("Введите слово, которое Вы добавляли себе:"),
        TextInput(
            id="search_word",
            on_success=event_handler.on_input_search_word,
        ),
        Row(
            buttons.HOME,
            Back(Const('Отмена')),
        ),
        state=AllWordSG.search_word,
    ),
    Window(
        Format("У вас нет слова {word}."),
        Button(
            Const("Найти в поиске"),
            id="new_word",
            #     TODO: Start(AddWordSG)
        ),
        Row(
            buttons.HOME,
            Back(Const('Назад')),
        ),
        state=AllWordSG.not_found_word,
        getter=getters.get_msg,
    ),
    on_start=event_handler.on_start,
    on_process_result=event_handler.process_collection_result,
)
