from dialogs.all_words.interface import DialogManager


async def get_msg(**kwargs) -> dict[str, str]:
    manager: DialogManager = kwargs['dialog_manager']
    dto = manager.dto
    words_text = [word.word for word in dto.word_list]
    text = ' \n'.join(words_text)
    return {
        'word_list': text,
    }
