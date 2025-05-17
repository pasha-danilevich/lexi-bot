from faker import Faker

from services.user.schemas import User
from services.user.service import UserScoped
from services.word.interface import IWordService
from services.word.schemas import UserWordCard, Word, WordCard

faker = Faker()
faker_ru = Faker('ru')
WORDS = [Word(word_id=faker.random_int(), text=faker.word()) for i in range(30)]


# class WordCard(Word):
#     translation: str
#     usage_count: int
#     part_of_speech: Optional[str]
#     transcription: Optional[str]
#     synonyms: Optional[list[str]]
#     antonyms: Optional[list[str]]
#
#     audio: Optional[str]
#     image: Optional[str]
#
#     usage_example: Optional[str]
#
# class UserWordCard(WordCard):
#     collection: str
#     associations: str
#     review_level: int
#     next_review: int
class WordMockService(IWordService, UserScoped):
    async def get_word(self, word_id: int) -> Word:
        _ = self.user.id
        _ = word_id
        # TODO:
        return Word(word_id=faker.random_int(), text=faker.word())

    async def get_word_card(self, word_id: int) -> WordCard | UserWordCard:
        """WordCard - если слова нет у пользователя. В остальных случаях - UserWordCard"""
        _ = self.user.id
        if word_id == 999:  # будто это слово есть у пользователя
            word_card = UserWordCard(
                word_id=faker.random_int(),
                text=faker.word(),
                translation=faker_ru.word(),
                usage_count=faker.random_int(max=30),
                part_of_speech='noun',
                transcription='*trs*',
                synonyms=[word.text for word in WORDS[:10]],
                antonyms=[word.text for word in WORDS[:10]],
                audio='https:/НАМЕРЕННО БИТАЯ ССЫЛКА.ogg',
                image='https://i.pinimg.com/736x/a5/a8/91/a5a891aac028ed6a1d4eb8e2d2ae5f39.jpg',
                usage_example=faker.catch_phrase(),
                collection=faker_ru.word().title(),
                associations=faker_ru.catch_phrase(),
                review_level=3,
                next_review=1746195952,
            )
        else:
            word_card = WordCard(
                word_id=faker.random_int(),
                text=faker.word(),
                translation=faker_ru.word(),
                usage_count=faker.random_int(max=30),
                part_of_speech='noun',
                transcription='*trs*',
                synonyms=[word.text for word in WORDS[:10]],
                antonyms=[word.text for word in WORDS[:10]],
                audio='https:/НАМЕРЕННО БИТАЯ ССЫЛКА.ogg',
                image=None,
                usage_example=faker.catch_phrase(),
            )

        return word_card

    async def get_all_words(
        self, collection_id: int, limit: int, offset: int
    ) -> list[Word]:
        _ = self.user.id
        _ = collection_id  # нужна фильтрация по коллекциям

        return WORDS[offset : offset + limit]


async def run():
    user = User(id=1237)
    serv = WordMockService(user=user)
    print(await serv.get_word(234))
    print(await serv.get_all_words(collection_id=123, limit=10, offset=10))


if __name__ == '__main__':
    import asyncio

    asyncio.run(run())
