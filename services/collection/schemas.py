from pydantic import BaseModel, Field


class CollectionDTO(BaseModel):
    """Коллекция в которой хранятся слова"""

    id: int
    name: str = Field(..., description="Имя коллекции")
    description: str
    is_default: bool
    is_public: bool
