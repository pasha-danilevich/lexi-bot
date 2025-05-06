from dialogs.collections.interface import DialogManager
from widgets.buttons import ButtonsGetter


async def get_buttons(**kwargs) -> ButtonsGetter:
    manager: DialogManager = kwargs['dialog_manager']
    collections = await manager.service.get_collections()
    return {
        "buttons": [(collection.name, collection.id) for collection in collections],
    }


async def get_msg(**kwargs):
    return {
        "text": 'hello',
    }
