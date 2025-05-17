from aiogram.enums import ContentType
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.api.entities.context import DataDict

from .interface import DialogManager


async def get_msg(**kwargs) -> DataDict:
    manager: DialogManager = kwargs['dialog_manager']
    dto = manager.dto

    data = {
        'word_card': dto.word_card,
        'user_word_card': dto.user_word_card,
    }

    image_url = getattr(dto.user_word_card, 'image', None)
    if image_url:
        image = MediaAttachment(ContentType.PHOTO, url=dto.user_word_card.image)
        data['image'] = image

    return data
