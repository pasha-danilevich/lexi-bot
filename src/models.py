from datetime import datetime, timezone

import jwt


class User:
    def __init__(self, user_data):
        self.id: int = user_data[0]
        self.tg_user_id: int = user_data[1]
        self.access_token: str = user_data[
            2
        ]  # Исправлено на правильный индекс для access_token

    def is_correct_access_token(self) -> bool:
        """Проверка JWT access_token на истечение срока."""
        try:
            # Декодируем токен, чтобы получить его payload
            payload = jwt.decode(
                self.access_token, options={"verify_signature": False}
            )  # Не проверяем подпись для проверки срока

            exp = payload.get(
                "exp"
            )  # Получаем время истечения срока действия токена

            if exp is None:
                return False  # Если 'exp' отсутствует,
            # токен считается недействительным

            # Проверяем, не истек ли токен
            expiration_time = datetime.fromtimestamp(exp, tz=timezone.utc)
            return expiration_time > datetime.now(tz=timezone.utc)
        except jwt.ExpiredSignatureError:
            return False  # Токен истек
        except jwt.InvalidTokenError:
            return False  # Неверный токен
        

class Word:
    def __init__(self) -> None:
        pass