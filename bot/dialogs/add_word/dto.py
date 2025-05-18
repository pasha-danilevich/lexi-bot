from typing import Optional

from pydantic import BaseModel

from services.word.schemas import UserWordCardDTO, WordCardDTO


class AddWordDTO(BaseModel):
    search_word: Optional[str] = None
    association: Optional[str] = None
    collection_id: Optional[int] = None
    # new word
    word_card: Optional[WordCardDTO | UserWordCardDTO] = None
    # user has this word
    user_word_card: Optional[UserWordCardDTO] = None
