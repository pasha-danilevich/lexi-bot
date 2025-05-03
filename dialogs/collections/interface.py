from dialog_manager.manager import CustomDialogManagerImpl
from services.collection.service import CollectionService


class DialogManager(CustomDialogManagerImpl):
    @property
    def service(self) -> CollectionService:
        return super().service
