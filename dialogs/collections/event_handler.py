from aiogram.types import CallbackQuery, Message
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Select

from services.collection.service import CollectionService
from services.user.schemas import User

from .dto import CollectionDTO
from .interface import DialogManager
from .state import CollectionSG


async def on_start(_, manager: DialogManager) -> None:
    user = User(id=manager.event.from_user.id)
    await manager.set_service(CollectionService(user=user))
    await manager.set_dto(CollectionDTO())


async def on_collection_selected(
    _: CallbackQuery, __: Select, manager: DialogManager, item_id: str
):
    await manager.done(result=item_id)


async def on_input_collection_name(
    _: Message, __: ManagedTextInput, manager: DialogManager, text: str
):
    manager.dto.name = text
    await manager.next()


async def create_without_description(
    _: CallbackQuery, __: Button, manager: DialogManager
):
    # TODO: Создание коллекции
    await manager.switch_to(CollectionSG.collections)


async def on_input_collection_description(
    _: Message, __: ManagedTextInput, manager: DialogManager, text: str
):
    manager.dto.description = text
    # TODO: Создание коллекции
    await manager.switch_to(CollectionSG.collections)
