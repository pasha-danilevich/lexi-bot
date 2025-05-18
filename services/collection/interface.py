from abc import abstractmethod

from services.collection.schemas import CollectionDTO
from services.user.interface import IUserScoped


class ICollection(IUserScoped):
    @abstractmethod
    async def get_collections(self) -> list[CollectionDTO]:
        raise NotImplementedError

    # @abstractmethod
    # async def create_collection(self) -> None:
    #     raise NotImplementedError
