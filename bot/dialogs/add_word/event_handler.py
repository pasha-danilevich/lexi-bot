from aiogram.types import Message
from aiogram_dialog.widgets.input import ManagedTextInput

from bot.dialogs.add_word.dto import AddWordDTO
from bot.dialogs.add_word.state import AddWordSG
from services.user.schemas import UserDTO
from services.word.schemas import UserWordCardDTO
from services.word.service import WordService

from .interface import DialogManager


async def on_start(_, manager: DialogManager) -> None:
    start_data = manager.start_data
    word: None | str = None

    if start_data:
        word = manager.start_data.get('word', None)

    user = UserDTO(telegram_id=manager.event.from_user.id)
    await manager.set_service(service=WordService(user))
    await manager.set_dto(AddWordDTO())

    if word:  # если слово пришло из вне
        # TODO: тут сервис ищет слово в mongo, либо создает новое слово
        word_id = (
            999 if word == 'my_word' else 123
        )  # если слово "my_word", то это слово, которое есть у пользователя
        await switch_window_base_on_user_word(word_id, manager)


async def switch_window_base_on_user_word(word_id: int, manager: DialogManager) -> None:
    """проверяет наличие слова у пользователя и возвращает соответствующее окно (состояние/экран)"""
    word_card = await manager.service.get_word_card(word_id)

    if isinstance(word_card, UserWordCardDTO):
        manager.dto.user_word_card = word_card
        await manager.switch_to(AddWordSG.user_word_card)
    else:
        manager.dto.word_card = word_card
        await manager.switch_to(AddWordSG.word_card)


async def on_input_search_word(
    _: Message, __: ManagedTextInput, manager: DialogManager, text: str
):
    manager.dto.search_word = text
    # TODO: тут сервис ищет слово в mongo, либо создает новое слово
    word_id = (
        999 if text == 'my_word' else 123
    )  # если слово "my_word", то это слово, которое есть у пользователя
    await switch_window_base_on_user_word(word_id, manager)
