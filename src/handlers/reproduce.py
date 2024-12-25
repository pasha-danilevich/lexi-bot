from typing import Any, cast

from aiogram import types
from aiogram.enums.parse_mode import ParseMode
from aiogram.utils import markdown
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import DOMAIN
from markup import buttons, keyboards
from markup.message import NON_AUTHORIZETE, TO_MANY_WORDS, REPRODUCE_TEXT
from models.word import Word
from state import Reproduce
from utils import (
    escape_markdown_v2,
    get_headers,
    get_response_data,
    get_response_data_post,
)


router = Router()

training_url = f"http://{DOMAIN}/api/training/?type=reproduce"


@router.callback_query(F.data == buttons.reproduce_test_cb_data)
async def reproduce_text_handler(callback: CallbackQuery, state: FSMContext):

    await callback.message.answer(  # type: ignore
        text=REPRODUCE_TEXT,
        reply_markup=keyboards.training_text,
    )


@router.callback_query(F.data == buttons.submit_training_cb_data)
async def reproduce_handler(callback: CallbackQuery, state: FSMContext):

    state_data = await state.get_data()
    access_token = state_data.get("access_token", None)

    message = cast(Message, callback.message)

    await state.set_state(Reproduce.text)

    if not access_token:
        await message.answer(text=NON_AUTHORIZETE)
        await state.set_state(None)
        return

    headers = await get_headers(access_token=access_token)

    if headers:
        json_data, status = await get_response_data(
            headers=headers, url=training_url
        )
        if not json_data:
            await message.answer(text=f"Ошибка: {status}")
            return
        print(json_data)
        # training_instance = Word.from_json(json_data)

        # await state.update_data(word_instance=word_instance)

        # text = display_info()
        await message.answer(
            text=f"f",
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=keyboards.reproduce,
        )


@router.message(Reproduce.text)
async def answer_reproduce_handler(message: Message, state: FSMContext):

    user_text: str | None = message.text

    await message.answer(  # type: ignore
        text=f"вы: {user_text}",
        # reply_markup=keyboards.reproduce,
    )
