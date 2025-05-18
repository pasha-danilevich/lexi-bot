from abc import ABC, abstractmethod

from db.tables import User
from services.user.schemas import UserIdentifier, UserSettings


class IUserScoped(ABC):
    def __init__(self, user_identifier: UserIdentifier):
        pass

    @abstractmethod
    async def get_settings(self) -> UserSettings:
        raise NotImplementedError()

    @abstractmethod
    async def get_user(self) -> User:
        raise NotImplementedError()
