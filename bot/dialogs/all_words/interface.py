from bot.dialog_manager.manager import CustomDialogManagerImpl
from bot.dialogs.all_words.dto import AllWordDTO
from services.word.service import WordService


class DialogManager(CustomDialogManagerImpl):
    @property
    def service(self) -> WordService:
        return super().service

    @property
    def dto(self) -> AllWordDTO:
        return super().dto
