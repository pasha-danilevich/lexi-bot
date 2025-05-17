from aiogram_dialog.api.entities.context import DataDict

from bot.dialogs.all_words.interface import DialogManager


async def get_msg(**kwargs) -> DataDict:
    manager: DialogManager = kwargs['dialog_manager']
    dto = manager.dto
    words_text = [word.text for word in dto.word_list]
    text = ' \n'.join(words_text)
    return {
        'word_list': text,
        'word': dto.search_word,
    }
