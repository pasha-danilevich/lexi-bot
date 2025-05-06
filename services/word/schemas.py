from typing import Optional

from pydantic import BaseModel, Field

from services.training.enums import TrainingType


class Word(BaseModel):
    word_id: int = Field(..., description="ID слова в базе")
    text: str = Field(..., min_length=1, description="Текст слова")


class WordCard(Word):
    translation: str
    usage_count: int
    part_of_speech: Optional[str]
    transcription: Optional[str]
    synonyms: Optional[list[str]]
    antonyms: Optional[list[str]]

    audio: Optional[str]
    image: Optional[str]

    usage_example: Optional[str]


class UserWordCard(WordCard):
    collection: str
    associations: str
    review_level: int
    next_review: int


class MistakeWord(BaseModel):
    """Схема для слова с ошибкой."""

    word: Word
    mistake_count: int = Field(..., ge=1, description="Количество ошибок")
    in_training_type: TrainingType = Field(
        ..., description="Тип упражнения, где была ошибка"
    )
