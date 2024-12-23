from typing import Any

from aiogram.enums.parse_mode import ParseMode
from aiogram.utils import markdown
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import DOMAIN
import keyboards
from message import NON_AUTHORIZETE
from utils import get_headers, get_response_data, get_user


router = Router()

training_url = f"http://{DOMAIN}/api/training/info/"


@router.message(Command("training"))
@router.callback_query(F.data == keyboards.training_cb_data)
async def training_handler(message_or_callback: Message | CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    access_token = state_data.get("access_token", None)

    if not access_token:
        await message_or_callback.answer(text=NON_AUTHORIZETE)
        return

    headers = await get_headers(access_token=access_token)

    if headers:
        training_data = await get_response_data(headers, training_url)
        training_info = await display_training_info(training_data)

        
        if isinstance(message_or_callback, Message):
            await message_or_callback.answer(
                text=training_info,
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=keyboards.training,
            )
        elif isinstance(message_or_callback, CallbackQuery):
            await message_or_callback.message.edit_text( # type: ignore
                text=training_info,
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=keyboards.training,
            )
            await message_or_callback.answer()  # Подтверждаем нажатие кнопки


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