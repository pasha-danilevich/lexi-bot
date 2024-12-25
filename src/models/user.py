from aiogram.types import Message
from utils import check_access_token


class User:
    def __init__(self, message: Message):
        from main import db

        self.db = db

        user_data = self.get_user_data_from_db(message)

        if user_data:
            self.id: int = user_data[0]
            self.tg_user_id: int = user_data[1]
            self.access_token: str = user_data[2]
        else:
            return None

    def get_user_data_from_db(self, message: Message):

        user_id = message.from_user.id  # type: ignore
        user_data = self.db.get_user(tg_user_id=user_id)
        return user_data

    def get_access_token(self):
        return self.access_token

    def update_access_token(self, new_access_token: str) -> None:
        self.db.edit_access_token(
            tg_user_id=self.tg_user_id, new_access_token=new_access_token
        )

    def create_new(self, access_token: str) -> None:
        self.db.add_user(
            tg_user_id=self.tg_user_id,
            access_token=access_token,
        )

    def is_correct_access_token(self) -> bool:
        """Проверка JWT access_token на истечение срока."""
        return check_access_token(self.access_token)
