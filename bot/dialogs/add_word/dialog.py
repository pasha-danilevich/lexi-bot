from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Back, Button, Row, SwitchTo
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format

from ..common import buttons
from . import event_handler, getters
from .state import AddWordSG

word_card_widgets = ()

word_card_windows = (
    Window(
        Format("{word_card}."),
        SwitchTo(
            Const("Добавить слово"),
            id="add_word",
            state=AddWordSG.select_collection,
        ),
        Row(
            buttons.HOME,
            SwitchTo(Const('Найти еще'), id="new_search", state=AddWordSG.add_word),
        ),
        state=AddWordSG.word_card,
        getter=getters.get_msg,
    ),
    Window(
        Format("{user_word_card}."),
        DynamicMedia("image"),
        SwitchTo(
            Const("Удалить слово"),
            id="delete_word",
            state=AddWordSG.delete_word,
        ),
        Row(
            buttons.HOME,
        ),
        state=AddWordSG.user_word_card,
        getter=getters.get_msg,
    ),
)

dialog = Dialog(
    Window(
        Const("Введите слово или предложение:"),
        TextInput(
            id="search_word",
            on_success=event_handler.on_input_search_word,
        ),
        buttons.HOME,
        state=AddWordSG.add_word,
    ),
    *word_card_windows,
    Window(
        Const("Слово необходимо поместить в коллекцию.."),
        SwitchTo(
            Const("Выбрать по умолчанию"),
            id="select_default",
            state=AddWordSG.select_collection,
        ),
        Row(
            buttons.HOME,
            Back(Const('Назад')),
        ),
        state=AddWordSG.select_collection,
    ),
    Window(
        Format(
            'Вы уверены, что хотите удалить "{user_word_card.text} - lvl:'
            ' {user_word_card.review_level} - association'
            ' {user_word_card.associations}" навсегда'
        ),
        Button(
            Const("Отложить слово на 1 месяц"),
            id="delay",
        ),
        Button(
            Const("Да, удалить"),
            id="delete",
        ),
        Row(
            buttons.HOME,
        ),
        getter=getters.get_msg,
        state=AddWordSG.delete_word,
    ),
    on_start=event_handler.on_start,
)
