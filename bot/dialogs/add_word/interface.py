from typing import TypedDict

from bot.dialog_manager.manager import CustomDialogManagerImpl
from bot.dialogs.add_word.dto import AddWordDTO
from services.word.service import WordService


class IStartData(TypedDict):
    word: str


class DialogManager(CustomDialogManagerImpl):
    @property
    def service(self) -> WordService:
        return super().service

    @property
    def dto(self) -> AddWordDTO:
        return super().dto

    @property
    def start_data(self) -> IStartData:
        """Start data for current context."""
        return self.current_context().start_data
