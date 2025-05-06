from typing import TypedDict, TypeVar, Union

from aiogram_dialog.widgets.kbd import Select
from aiogram_dialog.widgets.kbd.select import OnItemClick
from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.widget_event import WidgetEventProcessor

T = TypeVar("T")

Button = tuple[str, int]


# Определяем тип словаря с обязательным ключом "button"
class ButtonsGetter(TypedDict):
    buttons: list[Button]


class DynamicButtons(Select):
    def __init__(
        self,
        on_click: Union[
            OnItemClick["Select[T]", T],
            WidgetEventProcessor,
            None,
        ] = None,
    ):
        super().__init__(
            text=Format("{item[0]}"),
            id=f'{on_click.__name__[:-10]}',
            item_id_getter=lambda x: x[1],
            items='buttons',
            on_click=on_click,
        )
