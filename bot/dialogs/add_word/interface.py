from bot.dialog_manager.manager import CustomDialogManagerImpl
from bot.dialogs.add_word.dto import AddWordDTO
from services.word.service import WordService


class DialogManager(CustomDialogManagerImpl):
    @property
    def service(self) -> WordService:
        return super().service

    @property
    def dto(self) -> AddWordDTO:
        return super().dto
