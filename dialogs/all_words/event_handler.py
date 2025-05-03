from dialogs.all_words.dto import AllWordDTO
from dialogs.all_words.interface import DialogManager
from services.user.schemas import User
from services.word.service import WordService


async def on_start(_, manager: DialogManager) -> None:
    user = User(id=manager.event.from_user.id)
    await manager.set_service(service=WordService(user))
    words = await manager.service.get_all_words(limit=10, offset=0)
    await manager.set_dto(
        dto=AllWordDTO(
            word_list=words,
        )
    )
