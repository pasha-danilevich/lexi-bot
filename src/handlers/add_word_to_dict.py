from typing import Any, cast

from aiogram import types
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils import markdown

from markup import buttons, keyboards
from config import DOMAIN
from markup.message import NON_AUTHORIZETE
from models import Translation, Word
from utils import get_headers, get_response_data_post


router = Router()

add_word = f"http://{DOMAIN}/api/vocabulary/"


@router.callback_query(F.data == buttons.select_word_to_add_cd_data)
async def select_word_to_add(callback: types.CallbackQuery, state: FSMContext):

    message_text = "Какое слово добавить в словарь:"
    message = cast(Message, callback.message)

    state_data = await state.get_data()
    word_instance: Word = state_data.get("word_instance", None)

    await message.answer(
        text=message_text,
        reply_markup=keyboards.get_translation_list(
            translations=word_instance.translations,
            related_pk=word_instance.related_pk,
        ),
    )


@router.callback_query(F.data.startswith("translation_list_cd_data_pk_"))
async def add_word_to_dict(callback: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    access_token = state_data.get("access_token", None)
    message = cast(Message, callback.message)

    if not access_token:
        await message.answer(text=NON_AUTHORIZETE)
        return

    translation_pk = int(callback.data.split("_")[-1])  # type: ignore
    word_instance: Word = state_data.get("word_instance", None)
    message_text = ""

    translation: Translation | None = word_instance.get_translation(
        pk=translation_pk
    )

    headers = await get_headers(access_token=access_token)

    if headers and translation:
        data = make_post_data(
            word_pk=word_instance.pk, translation_pk=translation.pk
        )
        _, status = await get_response_data_post(
            headers=headers, url=add_word, data=data
        )
        if status == 201:
            message_text = (
                f"Добавленно новое слово: {markdown.bold(translation.text)}"
            )
        else:
            message_text = f"Слово уже добавленно\\."

    await message.answer(
        text=message_text,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=keyboards.word_added,
    )


def make_post_data(word_pk: int, translation_pk: int):
    data = {"word": word_pk, "translation": translation_pk}
    return data
