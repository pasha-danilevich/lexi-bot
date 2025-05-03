from pydantic import BaseModel, Field

from services.training.enums import TrainingType


class Word(BaseModel):
    word_id: int = Field(..., description="ID слова в базе")
    word: str = Field(..., min_length=1, description="Текст слова")


class MistakeWord(BaseModel):
    """Схема для слова с ошибкой."""

    word: Word
    mistake_count: int = Field(..., ge=1, description="Количество ошибок")
    in_training_type: TrainingType = Field(
        ..., description="Тип упражнения, где была ошибка"
    )
