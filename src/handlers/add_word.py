from typing import Any, cast

from aiogram import types
from aiogram.enums.parse_mode import ParseMode
from aiogram.utils import markdown
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import DOMAIN
from markup import buttons, keyboards
from markup.message import NON_AUTHORIZETE, TO_MANY_WORDS
from models.word import Word
from state import AddWord
from utils import (
    escape_markdown_v2,
    get_headers,
    get_response_data_post,
)


router = Router()

word_url = f"http://{DOMAIN}/api/words/"


@router.message(Command("add_word"))
@router.callback_query(F.data == buttons.add_word_cb_data)
async def add_word_handler(
    message_or_callback: Message | types.CallbackQuery, state: FSMContext
):
    await state.set_state(AddWord.text)
    message_text = "Введите слово на английском:"

    if isinstance(message_or_callback, Message):
        await message_or_callback.answer(
            text=message_text,
            reply_markup=keyboards.add_word,
        )
    elif isinstance(message_or_callback, types.CallbackQuery):
        await message_or_callback.message.answer(  # type: ignore
            text=message_text,
            reply_markup=keyboards.add_word,
        )
        await message_or_callback.answer()  # Подтверждаем нажатие кнопки


@router.message(AddWord.text)
async def translate_word_handler(message: Message, state: FSMContext):

    state_data = await state.get_data()
    access_token = state_data.get("access_token", None)
    user_text: str | None = message.text

    if user_text:
        if len(user_text.split(" ")) > 1:
            await message.answer(
                text=TO_MANY_WORDS, reply_markup=keyboards.word_added
            )
            await state.set_state(None)
            return

    if not access_token:
        await message.answer(text=NON_AUTHORIZETE)
        await state.set_state(None)
        return

    headers = await get_headers(access_token=access_token)

    if headers and user_text:
        json_data, _ = await get_response_data_post(
            headers=headers, url=word_url, data=make_post_data(user_text)
        )
        if not json_data:
            await message.answer(text="Ошибка")
            return

        word_instance = Word.from_json(json_data)

        await state.update_data(word_instance=word_instance)

        text = display_info(word=word_instance)
        await message.answer(
            text=text,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=keyboards.word_info,
        )

    await state.set_state(None)


def make_post_data(text: str) -> dict:
    return {"word": text}


def display_info(word: Word) -> str:
    translation_list = ""
    local_related_pk_list = word.related_pk.copy()

    for index, translation in enumerate(word.translations, start=1):
        if translation.pk in local_related_pk_list:
            translation_list += f"{index}. {translation.text} (в словаре)\n"
            local_related_pk_list.remove(translation.pk)
        else:
            translation_list += f"{index}. {translation.text}\n"

    synonym_list = []

    for synonym in word.synonyms:
        synonym_list.append(synonym.text)

    meaning_list = []

    for meaning in word.meanings:
        meaning_list.append(meaning.text)

    # Форматирование строки для вывода
    text = f"{markdown.bold(word.text)} \n"

    if word.transcription is not None:
        text += (
            f"\\[ {word.transcription} \\] {word.part_of_speech}\\. \n" f"\n"
        )

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
