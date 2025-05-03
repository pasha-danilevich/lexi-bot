from abc import ABC, abstractmethod

from services.user.schemas import User, UserSettings


class IUserScoped(ABC):
    def __init__(self, user: User):
        self.user = user

    @abstractmethod
    async def get_settings(self) -> UserSettings:
        raise NotImplementedError()
