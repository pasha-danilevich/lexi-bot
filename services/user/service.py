from db.tables import User
from services.user.interface import IUserScoped
from services.user.schemas import UserIdentifier, UserSettings


class UserScoped(IUserScoped):
    def __init__(self, user_identifier: UserIdentifier):
        super().__init__(user_identifier)

        self._user_id = user_identifier.user_id
        self._telegram_id = user_identifier.telegram_id
        self._email = user_identifier.email
        self._user: User | None = None

    async def get_settings(self) -> UserSettings:
        return UserSettings()

    async def get_user(self) -> User:
        if self._user:
            return self._user

        if self._user_id:
            self._user = await User.get_or_none(id=self._user_id)
        elif self._telegram_id:
            self._user = await User.get_or_none(telegram_id=self._telegram_id)
        elif self._email:
            self._user = await User.get_or_none(email=self._email)

        if not self._user:
            raise Exception("User not found by provided credentials")

        return self._user


async def run():
    from db.database import init_db

    await init_db()
    service = UserScoped(user_identifier=UserIdentifier(telegram_id=850472798))
    print(await service.get_user())


if __name__ == '__main__':
    import asyncio

    asyncio.run(run())
