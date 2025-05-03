from services.user.interface import IUserScoped
from services.user.schemas import User, UserSettings


class UserScoped(IUserScoped):
    def __init__(self, user: User):
        super().__init__(user)

    async def get_settings(self) -> UserSettings:
        return UserSettings()
