from typing import Any

from aiogram.enums.parse_mode import ParseMode
from aiogram.utils import markdown
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

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
async def add_word_handler(message: Message, state: FSMContext):
    await state.set_state(AddWord.text)

    await message.answer("Введите слово на английском:")


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
        await message.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)


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
        f"\\[ {word.transcription} \\] {word.part_of_speech}\\. \n"
        f"\n"
        f"{markdown.italic('Перевод:')} \n"
        f"{escape_markdown_v2(translation_list)}"
        f"\n"
        f"{markdown.italic('Синонимы:')} \n"
        f"{escape_markdown_v2(', '.join(synonym_list))} \n"
        f"\n"
        f"{markdown.italic('Близкие по значению:')} \n"
        f"{escape_markdown_v2(', '.join(meaning_list))} \n"
        f"\n"
        f"{markdown.bold()}"
    )

    return text



