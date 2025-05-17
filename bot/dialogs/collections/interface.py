from bot.dialog_manager.manager import CustomDialogManagerImpl
from bot.dialogs.collections.dto import CollectionDTO
from services.collection.service import CollectionService


class DialogManager(CustomDialogManagerImpl):
    @property
    def service(self) -> CollectionService:
        return super().service

    @property
    def dto(self) -> CollectionDTO:
        return super().dto
