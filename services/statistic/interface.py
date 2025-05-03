from abc import ABC, abstractmethod

from services.statistic.schema import UserStatsResponse


class IStatistic(ABC):
    @abstractmethod
    async def get(self, user_id: int) -> UserStatsResponse:
        raise NotImplementedError

    @abstractmethod
    async def update_total_words(self, user_id: int):
        raise NotImplementedError
