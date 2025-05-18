from services.user.service import UserScoped
from services.word.interface import IWordService
from services.word.schemas import UserWordCardDTO, WordCardDTO, WordDTO


class WordService(IWordService, UserScoped):
    async def get_word_card(self, word_id: int) -> WordCardDTO | UserWordCardDTO:
        """WordCard - если слова нет у пользователя. В остальных случаях - UserWordCard"""

    async def get_all_words(self, limit: int = 10, offset: int = 0) -> list[WordDTO]:
        user = await self.get_user()
        words = [
            WordDTO(word_id=word.id, text=word.word_text)
            for word in await user.user_words.offset(offset).limit(limit).all()
        ]
        return words

    def __str__(self):
        return self.__class__.__name__


async def run():
    from db.database import init_db
    from services.user.schemas import UserIdentifier

    await init_db()
    service = WordService(user_identifier=UserIdentifier(telegram_id=850472798))
    print(await service.get_all_words())


if __name__ == '__main__':
    import asyncio

    asyncio.run(run())
