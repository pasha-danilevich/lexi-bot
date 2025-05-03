from dialogs.collections.interface import DialogManager


async def get_buttons(**kwargs):
    manager: DialogManager = kwargs['dialog_manager']
    collections = await manager.service.get_collections()
    return {
        "buttons": [(collection.name, collection.id) for collection in collections],
    }
