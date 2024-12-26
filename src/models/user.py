from aiogram.types import Message

from utils import check_access_token
from database import UserTuple


class User:
    def __init__(self, message: Message, user: UserTuple):
        self.id = user.id
        self.tg_user_id = user.tg_user_id
        self.access_token: str | None = user.access_token

    def get_access_token(self):
        return self.access_token

    def is_correct_access_token(self) -> bool:
        """Проверка JWT access_token на истечение срока."""
        if not self.access_token:
            return False

        return check_access_token(self.access_token)
