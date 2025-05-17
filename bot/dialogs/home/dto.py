from typing import Optional

from pydantic import BaseModel


class HomeDTO(BaseModel):
    total_words: Optional[int] = None
