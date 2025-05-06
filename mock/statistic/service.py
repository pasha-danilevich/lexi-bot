from services.statistic.interface import IStatistic
from services.statistic.schemas import UserStatsResponse
from services.training.enums import TrainingType
from services.user.schemas import User
from services.user.service import UserScoped
from services.word.schemas import MistakeWord, Word


class StatisticMockService(IStatistic, UserScoped):
    words_db = [
        Word(word_id=13342345, text="hello"),
        Word(word_id=45345, text="home"),
        Word(word_id=657567, text="acquire"),
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

    async def get_statistic(self) -> UserStatsResponse:
        print(f'{self.user.id=}')
        return UserStatsResponse(**self.mock_db)

    async def update_total_words(self, count: int) -> None:
        self.mock_db[0]['total_words'] = count


async def run():
    user = User(id=123)
    mock = StatisticMockService(user)
    print(await mock.get_statistic())
    await mock.update_total_words(50)
    print(await mock.get_statistic())


if __name__ == '__main__':
    import asyncio

    asyncio.run(run())
