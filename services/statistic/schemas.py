from datetime import datetime
from typing import Dict, List

from pydantic import BaseModel, Field

from services.word.schemas import MistakeWord, WordDTO


class UserStatsResponse(BaseModel):
    """Полная статистика пользователя."""

    total_words: int = Field(..., ge=0, description="Общее количество изученных слов")
    total_sessions: int = Field(..., ge=0, description="Всего тренировок")

    levels: Dict[str, int] = Field(
        ...,
        description="Количество слов на каждом уровне сложности ",
        json_schema_extra={"example": {"1": 25, "2": 40}},
    )

    mistakes: List[MistakeWord] = Field(
        ..., max_length=10, description="Топ-10 слов с наибольшим количеством ошибок"
    )
    recent: List[WordDTO] = Field(
        ..., max_length=5, description="Недавно добавленные слова"
    )

    last_session: datetime = Field(
        ...,
        description="Дата и время последней тренировки в UTC",
        examples=["2025-04-30T14:30:00Z"],
    )

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 850472798,
                "total_words": 150,
                "total_sessions": 42,
                "levels": {"1": 25, "2": 40, "3": 35, "4": 30, "5": 20},
                "mistakes": [
                    {
                        "word": {"word_id": 13342345, "word": "acquire"},
                        "mistake_count": 12,
                        "in_review_type": "translate",
                    }
                ],
                "recent": [
                    {
                        "word_id": 13342345,
                        "word": "hello",
                    },
                    {
                        "word_id": 13342345,
                        "word": "home",
                    },
                ],
                "last_session": "2025-04-30T14:30:00Z",
            }
        }
