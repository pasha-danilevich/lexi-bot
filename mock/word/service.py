from faker import Faker

from services.user.schemas import User
from services.user.service import UserScoped
from services.word.interface import IWordService
from services.word.schemas import Word

faker = Faker()


class WordMockService(IWordService, UserScoped):
    async def get_word(self) -> Word:
        user_id = self.user.id
        return Word(word_id=faker.random_int(), word=faker.word())

    async def get_all_words(self, limit: int, offset: int) -> list[Word]:
        _ = self.user.id

        words = [Word(word_id=faker.random_int(), word=faker.word()) for i in range(30)]
        return words[offset : offset + limit]


async def run():
    user = User(id=1237)
    serv = WordMockService(user=user)
    print(await serv.get_word())
    print(await serv.get_all_words(limit=10, offset=10))


if __name__ == '__main__':
    import asyncio

    asyncio.run(run())
