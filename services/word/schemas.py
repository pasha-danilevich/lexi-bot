from typing import Optional

from pydantic import BaseModel, Field

from services.training.enums import TrainingType


class WordDTO(BaseModel):
    """Слово, которое связанно с пользователем. Находится в Postgres, поэтому данные без справочной информации из Mongo"""

    word_id: int = Field(..., description="ID слова в базе")
    text: str = Field(..., min_length=1, description="Текст слова")


class WordCardDTO(WordDTO):
    translation: str
    usage_count: int
    part_of_speech: Optional[str]
    transcription: Optional[str]
    synonyms: Optional[list[str]]
    antonyms: Optional[list[str]]

    audio: Optional[str]
    image: Optional[str]

    usage_example: Optional[str]


class UserWordCardDTO(WordCardDTO):
    collection: str
    associations: str
    review_level: int
    next_review: int


class MistakeWord(BaseModel):
    """Схема для слова с ошибкой."""

    word: WordDTO
    mistake_count: int = Field(..., ge=1, description="Количество ошибок")
    in_training_type: TrainingType = Field(
        ..., description="Тип упражнения, где была ошибка"
    )
