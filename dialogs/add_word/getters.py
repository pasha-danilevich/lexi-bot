from aiogram.enums import ContentType
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.api.entities.context import DataDict

from .interface import DialogManager


async def get_msg(**kwargs) -> DataDict:
    manager: DialogManager = kwargs['dialog_manager']
    dto = manager.dto
    image = MediaAttachment(ContentType.PHOTO, url=dto.user_word_card.image)

    return {
        'word_card': dto.word_card,
        'user_word_card': dto.user_word_card,
        'image': image,
    }
