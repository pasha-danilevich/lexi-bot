# src/utils.py


from typing import Any
from aiogram.types import Message
import aiohttp

from database import Database
from models import User


def format_message(text: str, format_type: str) -> str:
    switcher = {
        "bold": f"**{text}**",  # Жирный текст
        "spoiler": f"||{text}||",  # Спойлер
        "italic": f"*{text}*",  # Курсив
        "underline": f"__{text}__",  # Подчеркнутый текст
        "strikethrough": f"~~{text}~~",  # Зачеркнутый текст
    }

    return switcher.get(
        format_type, text
    )  # Возвращает текст без изменений, если формат не найден


def escape_markdown_v2(text):
    """Экранирует специальные символы для MarkdownV2."""
    escape_chars = r"_ * [ ] ( ) ~ ` > # + - = | { } . !".split()
    for char in escape_chars:
        text = text.replace(char, f"\\{char}")
    return text


async def get_user(message: Message, db: Database) -> User | None:
    if message.from_user:
        user_id = message.from_user.id

    user_data = db.get_user(tg_user_id=user_id)

    if user_data:
        user = User(user_data=user_data)
    else:
        user = None

    return user


async def get_response_data(headers, url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                print(f"Ошибка: {response.status}")
                return None


import aiohttp


async def get_response_data_post(headers, url: str, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status in [200, 201]:
                data = await response.json()
                return data
            else:
                print(f"Ошибка: {response.status}")
                return None


async def get_headers(access_token: str | Any | None) -> dict[str, str] | None:
    if access_token is not None:
        headers = {"Authorization": f"Beare {access_token}"}
        return headers
    else:
        return None
