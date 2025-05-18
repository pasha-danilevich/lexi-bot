from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Data
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button
from loguru import logger

from bot.dialogs.add_word.state import AddWordSG
from bot.dialogs.all_words.dto import AllWordDTO
from bot.dialogs.all_words.interface import DialogManager
from bot.dialogs.all_words.state import AllWordSG
from bot.dialogs.collections.state import CollectionSG
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


async def on_input_search_word(
    _: Message, __: ManagedTextInput, manager: DialogManager, text: str
):
    manager.dto.search_word = text
    logger.debug(text)
    # TODO: Пытаемся найти слово у пользователя

    if text == 'my_word':  # считаем, что слово найдено
        await manager.start(AddWordSG.add_word, data={'word': manager.dto.search_word})
    else:  # считаем, что слово не найдено
        await manager.switch_to(AllWordSG.not_found_word)


async def on_found_word_in_search(_: CallbackQuery, __: Button, manager: DialogManager):
    logger.debug(manager.dto.search_word)
    await manager.start(AddWordSG.add_word, data={'word': manager.dto.search_word})
