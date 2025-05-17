from bot.dialog_manager.manager import CustomDialogManagerImpl
from bot.dialogs.home.dto import HomeDTO
from services.statistic.interface import IStatistic


class DialogManager(CustomDialogManagerImpl):
    @property
    def service(self) -> IStatistic:
        return super().service

    @property
    def dto(self) -> HomeDTO:
        return super().dto
