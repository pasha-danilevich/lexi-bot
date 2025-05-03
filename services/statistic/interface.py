from abc import abstractmethod

from services.statistic.schemas import UserStatsResponse
from services.user.interface import IUserScoped


class IStatistic(IUserScoped):
    @abstractmethod
    async def get_statistic(self) -> UserStatsResponse:
        raise NotImplementedError

    @abstractmethod
    async def update_total_words(self, count: int) -> None:
        raise NotImplementedError
