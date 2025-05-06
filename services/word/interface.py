from abc import abstractmethod

from services.user.interface import IUserScoped
from services.word.schemas import UserWordCard, Word, WordCard


class IWordService(IUserScoped):
    @abstractmethod
    async def get_word(self, word_id: int) -> Word:
        raise NotImplementedError

    @abstractmethod
    async def get_word_card(self, word_id: int) -> WordCard | UserWordCard:
        raise NotImplementedError

    @abstractmethod
    async def get_all_words(
        self, collection_id: int, limit: int, offset: int
    ) -> list[Word]:
        raise NotImplementedError
