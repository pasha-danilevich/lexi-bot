# src/user.py

from dataclasses import dataclass


@dataclass
class User:
    email: str
    username: str
    password: str


# Предположим, что у вас есть сохраненный хеш пароля из базы данных
stored_password_hash = ""

# Введенный пользователем пароль
entered_password = ""

# Проверка пароля
# if django_pbkdf2_sha256.verify(entered_password, stored_password_hash):
#     print("Пароль верный!")
# else:
#     print("Пароль неверный.")
