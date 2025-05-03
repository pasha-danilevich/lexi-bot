from dialogs.home.interface import DialogManager


async def get_msg(**kwargs) -> dict[str, int]:
    manager: DialogManager = kwargs['dialog_manager']
    dto = manager.dto
    return {
        'total_words': dto.total_words,
    }
