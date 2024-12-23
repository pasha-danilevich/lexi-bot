import random
from typing import Any, cast

from aiogram import types
from aiogram.enums.parse_mode import ParseMode
from aiogram.utils import markdown
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import keyboards
from config import DOMAIN
from message import NON_AUTHORIZETE
from models import Word
from state import AddWord
from utils import (
    escape_markdown_v2,
    get_headers,
    get_response_data,
    get_response_data_post,
    get_user,
)


router = Router()

word_url = f"http://{DOMAIN}/api/words/"


@router.message(Command("add_word"))
@router.callback_query(F.data == keyboards.add_word_cb_data)
async def add_word_handler(
    message_or_callback: Message | types.CallbackQuery, state: FSMContext
):
    await state.set_state(AddWord.text)
    message_text = "Введите слово на английском:"

    # await message_or_callback.answer("Введите слово на английском:")

    if isinstance(message_or_callback, Message):
        await message_or_callback.answer(
            text=message_text,
            reply_markup=keyboards.add_word,
        )
    elif isinstance(message_or_callback, types.CallbackQuery):
        await message_or_callback.message.edit_text(  # type: ignore
            text=message_text,
            reply_markup=keyboards.add_word,
        )
        await message_or_callback.answer()  # Подтверждаем нажатие кнопки


@router.message(AddWord.text)
async def translate_word_handler(message: Message, state: FSMContext):

    state_data = await state.get_data()
    access_token = state_data.get("access_token", None)
    user_text = message.text

    if not access_token:
        await message.answer(text=NON_AUTHORIZETE)
        return

    headers = await get_headers(access_token=access_token)

    if headers and user_text:
        json_data = await get_response_data_post(
            headers=headers, url=word_url, data=make_post_data(user_text)
        )
        if not json_data:
            await message.answer(text="Ошибка")
            return

        word_instance = Word.from_json(json_data)
        text = display_info(word=word_instance)
        await message.answer(
            text=text,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=keyboards.word_info,
        )
    
    await state.clear()  # Завершаем текущее состояние и очищаем данные


def make_post_data(text: str) -> dict:
    return {"word": text}


def display_info(word: Word) -> str:

    translation_list = ""

    for index, translation in enumerate(word.translations, start=1):
        translation_list += f"{index}. {translation.text}\n"

    synonym_list = []

    for synonym in word.synonyms:
        synonym_list.append(synonym.text)

    meaning_list = []

    for meaning in word.meanings:
        meaning_list.append(meaning.text)

    # Форматирование строки для вывода
    text = (
        f"{markdown.bold(word.text)} \n"
        f"\n"
    )
    
    if word.transcription is not None:
        text += f"\\[ {word.transcription} \\] {word.part_of_speech}\\. \n"
    
    text += (
        f"{markdown.italic('Перевод:')} \n"
        f"{escape_markdown_v2(translation_list)}"
    )
    
    synonym_text = (
        f"\n"
        f"{markdown.italic('Синонимы:')} \n"
        f"{escape_markdown_v2(', '.join(synonym_list))} \n"
    )
    if synonym_list:
        text += synonym_text

    meaning_text = (
        f"\n"
        f"{markdown.italic('Близкие по значению:')} \n"
        f"{escape_markdown_v2(', '.join(meaning_list))} \n"
    )

    if meaning_list:
        text += meaning_text

    return text
