from typing import Optional

from pydantic import BaseModel

from services.word.schemas import Word


class AllWordDTO(BaseModel):
    word_list: Optional[list[Word]] = None
