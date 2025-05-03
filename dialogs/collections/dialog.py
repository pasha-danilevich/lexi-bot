from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Group, Select
from aiogram_dialog.widgets.text import Const, Format

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
        state=CollectionSG.collections,
        getter=getters.get_buttons,
    ),
    on_start=event_handler.on_start,
)
