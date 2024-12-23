from typing import Any, cast

from aiogram import types
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import keyboards
from config import DOMAIN
from models import Word


router = Router()

add_word = f"http://{DOMAIN}"


@router.callback_query(F.data == keyboards.add_word_to_dict_cd_data)
async def add_word_to_dict(callback: types.CallbackQuery, state: FSMContext):

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