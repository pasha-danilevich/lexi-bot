# src/utils.py


from datetime import datetime, timezone
import inspect
from typing import Any, Tuple
from aiogram.types import Message
import aiohttp
import jwt

# from database import Database
# from models import User


def print_with_location(message: str):
    # Получаем информацию о текущем кадре
    frame = inspect.currentframe()

    # Получаем информацию о вызывающем кадре
    if frame:
        caller_frame = frame.f_back
        if caller_frame:
            # Получаем имя файла и номер строки
            filename = caller_frame.f_code.co_filename
            line_number = caller_frame.f_lineno

    # Формируем сообщение с указанием файла и строки
    print(f"{message} (File: {filename}, line {line_number})")


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


def check_access_token(access_token: str):
    """Проверка JWT access_token на истечение срока."""
    try:
        # Декодируем токен, чтобы получить его payload
        payload = jwt.decode(
            access_token, options={"verify_signature": False}
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


async def get_response_data(headers, url: str) -> Tuple[Any, int]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data, response.status
            else:
                print_with_location(f"Ошибка: {response.status}")
                return None, response.status


import aiohttp


async def get_response_data_post(
    headers: dict, url: str, data: dict
) -> Tuple[Any, int]:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                url, headers=headers, json=data
            ) as response:
                if response.status in [200, 201]:
                    data = await response.json()
                    return data, response.status
                else:
                    print_with_location(f"Ошибка: {response.status}")
                    return None, response.status
        except aiohttp.ClientError as e:
            print_with_location(f"Ошибка при выполнении запроса: {e}")
            return None, 500  # в случае ошибки запроса


async def get_response_data_patch(
    headers: dict, url: str, data: dict
) -> Tuple[Any, int]:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.patch(
                url, headers=headers, json=data
            ) as response:
                if response.status in [200, 201]:

                    return "", response.status
                else:
                    print_with_location(f"Ошибка: {response.status}")
                    return None, response.status
        except aiohttp.ClientError as e:
            print_with_location(f"Ошибка при выполнении запроса: {e}")
            return None, 500  # в случае ошибки запроса


async def get_headers(access_token: str | Any | None) -> dict[str, str] | None:
    if access_token is not None:
        headers = {"Authorization": f"Beare {access_token}"}
        return headers
    else:
        return None
