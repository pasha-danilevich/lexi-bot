from typing import Optional

from pydantic import BaseModel

from services.word.schemas import WordDTO


class AllWordDTO(BaseModel):
    word_list: Optional[list[WordDTO]] = None
    search_word: Optional[str] = None
