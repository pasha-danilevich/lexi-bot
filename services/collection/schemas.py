from pydantic import BaseModel, Field


class Collection(BaseModel):
    """Коллекция в которой хранятся слова"""

    id: int
    name: str = Field(..., description="Имя коллекции")
