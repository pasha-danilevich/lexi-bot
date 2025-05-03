from aiogram.types import CallbackQuery
from aiogram_dialog.widgets.kbd import Select

from services.collection.service import CollectionService
from services.user.schemas import User

from .interface import DialogManager


async def on_start(_, manager: DialogManager) -> None:
    user = User(id=manager.event.from_user.id)
    await manager.set_service(CollectionService(user=user))


async def on_collection_selected(
    _: CallbackQuery, __: Select, manager: DialogManager, item_id: str
):
    await manager.done(result=item_id)
