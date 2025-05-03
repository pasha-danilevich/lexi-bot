from abc import abstractmethod

from services.user.interface import IUserScoped
from services.word.schemas import Word


class IWordService(IUserScoped):
    @abstractmethod
    async def get_word(self) -> Word:
        raise NotImplementedError

    @abstractmethod
    async def get_all_words(
        self, collection_id: int, limit: int, offset: int
    ) -> list[Word]:
        raise NotImplementedError
