from abc import abstractmethod

from services.user.interface import IUserScoped
from services.word.schemas import UserWordCardDTO, WordCardDTO, WordDTO


class IWordService(IUserScoped):
    @abstractmethod
    async def get_word_card(self, word_id: int) -> WordCardDTO | UserWordCardDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_all_words(self, limit: int, offset: int) -> list[WordDTO]:
        raise NotImplementedError
