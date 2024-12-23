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

home_url = f"http://{DOMAIN}/api/home/"


@router.message(Command("my_profile"))
@router.callback_query(F.data == keyboards.profile_cd_data)
async def my_profile_handler(
    message_or_callback: Message | CallbackQuery, state: FSMContext
):
    state_data = await state.get_data()
    access_token = state_data.get("access_token", None)

    if not access_token:
        await message_or_callback.answer(text=NON_AUTHORIZETE)
        return

    headers = await get_headers(access_token=access_token)

    if headers:
        home_data = await get_response_data(headers, home_url)
        profile_info = await display_profile_info(home_data)

        if isinstance(message_or_callback, Message):
            await message_or_callback.answer(
                text=profile_info,
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=keyboards.my_profile,
            )
        elif isinstance(message_or_callback, CallbackQuery):
            await message_or_callback.message.edit_text(  # type: ignore
                text=profile_info,
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=keyboards.my_profile,
            )
            await message_or_callback.answer()  # Подтверждаем нажатие кнопки


async def display_profile_info(data) -> str:
    # Пример данных
    total_words = data["learning_words"]
    new_words_today = data["new_words_today"]

    # Форматирование строки для вывода
    profile_info = (
        f"{markdown.bold('Ваш профиль:')} \n"
        f"Всего слов: {markdown.bold(total_words)} \n"
        f"Новых слов за сегодня: {markdown.bold(new_words_today)} \n"
    )
    return profile_info
