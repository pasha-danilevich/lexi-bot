from aiogram.types import Message
from aiogram_dialog.widgets.input import ManagedTextInput

from dialogs.add_word.dto import AddWordDTO
from dialogs.add_word.state import AddWordSG
from services.user.schemas import User
from services.word.schemas import UserWordCard
from services.word.service import WordService

from .interface import DialogManager


async def on_start(_, manager: DialogManager) -> None:
    start_data = manager.start_data
    word = None

    if start_data:
        word = manager.start_data.get('word', None)

    user = User(id=manager.event.from_user.id)
    await manager.set_service(service=WordService(user))
    await manager.set_dto(AddWordDTO())

    if word:  # если слово пришло из вне
        word_id = 123  # TODO: тут сервис ищет слово в mongo, либо создает новое слово
        await switch_window_base_on_user_word(word_id, manager)


async def switch_window_base_on_user_word(word_id: int, manager: DialogManager) -> None:
    """проверяет наличие слова у пользователя и возвращает соответствующее окно (состояние/экран)"""
    word_card = await manager.service.get_word_card(word_id)

    if isinstance(word_card, UserWordCard):
        manager.dto.user_word_card = word_card
        await manager.switch_to(AddWordSG.user_word_card)
    else:
        manager.dto.word_card = word_card
        await manager.switch_to(AddWordSG.word_card)


async def on_input_search_word(
    _: Message, __: ManagedTextInput, manager: DialogManager, text: str
):
    manager.dto.search_word = text
    word_id = 123  # TODO: тут сервис ищет слово в mongo, либо создает новое слово
    await switch_window_base_on_user_word(word_id, manager)
