from services.statistic.interface import IStatistic
from services.statistic.schema import MistakeWord, UserStatsResponse, Word
from services.training.enums import TrainingType


class StatisticMockService(IStatistic):
    words_db = [
        Word(word_id=13342345, word="hello"),
        Word(word_id=45345, word="home"),
        Word(word_id=657567, word="acquire"),
    ]
    mock_db = {
        "user_id": 850472798,
        "total_words": 150,
        "total_sessions": 42,
        "levels": {"1": 25, "2": 40, "3": 35, "4": 30, "5": 20},
        "mistakes": [
            MistakeWord(
                mistake_count=12,
                in_training_type=TrainingType.CHOICE_QUIZ,
                word=words_db[2],
            )
        ],
        "recent": [words_db[0], words_db[1]],
        "last_session": "2025-04-30T14:30:00Z",
    }

    async def get(self, user_id: int) -> UserStatsResponse:
        return UserStatsResponse(**self.mock_db)

    async def update_total_words(self, count: int):
        self.mock_db[0]['total_words'] = count


async def run():
    mock = StatisticMockService()
    print(await mock.get(123))
    await mock.update_total_words(50)
    print(await mock.get(123))


if __name__ == '__main__':
    import asyncio

    asyncio.run(run())
