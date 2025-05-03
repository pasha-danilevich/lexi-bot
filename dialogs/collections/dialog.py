from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Group, Next, Row, Select, SwitchTo
from aiogram_dialog.widgets.text import Const, Format

from ..common import buttons
from . import event_handler, getters
from .state import CollectionSG

dialog = Dialog(
    Window(
        Const("Коллекции:"),
        Group(
            Select(
                Format("{item[0]}"),
                id="collection",
                item_id_getter=lambda x: x[1],  # ID из кортежа Button(text, id)
                items="buttons",
                on_click=event_handler.on_collection_selected,
            ),
            width=2,
        ),
        Next(Const("Создать коллекцию")),
        buttons.HOME,
        state=CollectionSG.collections,
        getter=getters.get_buttons,
    ),
    Window(
        Const("Введите название коллекции:"),
        TextInput(
            id="create_collection",
            on_success=event_handler.on_input_collection_name,
        ),
        Row(
            buttons.HOME,
            SwitchTo(Const('Отмена'), state=CollectionSG.collections, id='cancel'),
        ),
        state=CollectionSG.create_collection,
    ),
    Window(
        Const("Введите описание этой коллекции:"),
        TextInput(
            id="add_description",
            on_success=event_handler.on_input_collection_description,
        ),
        Button(
            Const("Создать без описания"),
            id="create_without_description",
            on_click=event_handler.create_without_description,
        ),
        Row(
            buttons.HOME,
            SwitchTo(Const('Отмена'), state=CollectionSG.collections, id='cancel'),
        ),
        state=CollectionSG.add_description,
    ),
    on_start=event_handler.on_start,
)
