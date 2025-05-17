from typing import Optional

from pydantic import BaseModel


class CollectionDTO(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
