from dialog_manager.manager import CustomDialogManagerImpl
from dialogs.home.dto import HomeDTO
from services.statistic.service import StatisticService


class DialogManager(CustomDialogManagerImpl):
    @property
    def service(self) -> StatisticService:
        return super().service

    @property
    def dto(self) -> HomeDTO:
        return super().dto
