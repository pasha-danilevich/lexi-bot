from typing import Any

import aiohttp
from aiogram.enums.parse_mode import ParseMode
from aiogram.utils import markdown
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import DOMAIN
from message import NON_AUTHORIZETE
from utils import get_headers, get_response_data, get_user


router = Router()

home_url = f"http://{DOMAIN}/api/home/"
training_url = f"http://{DOMAIN}/api/training/info/"


@router.message(Command("my_profile"))
async def my_profile_handler(message: Message, state: FSMContext):
    state_data = await state.get_data()
    access_token = state_data.get("access_token", None)

    if not access_token:
        await message.answer(text=NON_AUTHORIZETE)
        return

    headers = await get_headers(access_token=access_token)

    if headers:
        home_data = await get_response_data(headers, home_url)
        training_data = await get_response_data(headers, training_url)
        profile_info = await display_profile_info(home_data)
        training_info = await display_training_info(training_data)

        await message.answer(
            text=profile_info, parse_mode=ParseMode.MARKDOWN_V2
        )
        await message.answer(
            text=training_info, parse_mode=ParseMode.MARKDOWN_V2
        )


async def display_profile_info(data) -> str:
    # Пример данных
    total_words = data["learning_words"]
    added_books = data["upload_books"]
    new_words_today = data["new_words_today"]

    # Форматирование строки для вывода
    profile_info = (
        f"{markdown.bold('Ваш профиль:')} \n"
        f"Всего слов: {markdown.bold(total_words)} \n"
        f"Добавленных книг: {markdown.bold(added_books)} \n"
        f"Новых слов за сегодня: {markdown.bold(new_words_today)} \n"
    )
    return profile_info


async def display_training_info(data) -> str:

    words_to_repeat = (
        data["count_word_to_training_recognize"]
        + data["count_word_to_training_reproduce"]
    )
    choice_test_words = data["count_word_to_training_recognize"]
    reproduce_test_words = data["count_word_to_training_reproduce"]

    # Форматирование строки для вывода
    training_info = (
        f"Необходимо повторить {markdown.bold(words_to_repeat)} {markdown.bold('слов')} \n"
        f"Тест с выбором ответа: "
        f"{markdown.bold(choice_test_words)}\n"
        f"Тест на узнаваемость: "
        f"{markdown.bold(reproduce_test_words)}\n"
    )
    return training_info
