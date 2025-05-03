from aiogram_dialog import Data

from dialogs.all_words.dto import AllWordDTO
from dialogs.all_words.interface import DialogManager
from dialogs.collections.state import CollectionSG
from services.user.schemas import User
from services.word.service import WordService


async def on_start(_, manager: DialogManager) -> None:
    await manager.start(CollectionSG.collections)


async def process_collection_result(
    start_data: Data,
    result: int,
    manager: DialogManager,
):
    print("We have result from collection_dialog:", result)

    user = User(id=manager.event.from_user.id)
    await manager.set_service(service=WordService(user))
    words = await manager.service.get_all_words(
        collection_id=result, limit=10, offset=0
    )
    await manager.set_dto(
        dto=AllWordDTO(
            word_list=words,
        )
    )
