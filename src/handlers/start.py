# src/handler.py

import aiohttp
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from markup import message as text_message
from config import DOMAIN
from models.user import User
from utils import check_access_token


router = Router()
url = f"http://{DOMAIN}/api/tg-auth/"


@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):

    state_data = await state.get_data()
    access_token = state_data.get("access_token", None)

    if access_token:
        if check_access_token(access_token):
            await message.answer(text=text_message.ALREADY_AUTHORIZED)
        else:
            await message.answer(text=text_message.TOKEN_HAS_EXPIRED)
        return

    await message.answer(text=text_message.START_MESSEGE)

    if message.text:
        hash_code = await _get_hash(message_text=message.text)

        if hash_code:
            url_params = url + f"?hash={hash_code}"

            async with aiohttp.ClientSession() as session:
                async with session.get(url_params) as response:
                    if response.status == 200:
                        access_token = await response.json()

                        await state.update_data(access_token=access_token)
                    elif response.status == 404:
                        await message.answer(
                            text=text_message.ERROR_GET_ACCESS_TOKEN
                        )
                    else:
                        await message.answer(
                            text=text_message.UNEXPECTED_ERROR_GET_ACCESS_TOKEN
                        )

    user = User(message=message)

    if not access_token:

        if not user:
            await message.answer(text=text_message.YOU_ARE_FIRST)
        else:
            # актуален ли access_token у user

            if user.is_correct_access_token():
                await state.update_data(access_token=user.access_token)
                await message.answer(text=text_message.YOU_AUTH_MESSEGE)
            else:
                await message.answer(text=text_message.TOKEN_HAS_EXPIRED)
    else:
        await message.answer(text=text_message.YOU_AUTH_MESSEGE)
        user.update_access_token(access_token)

        if not user:
            from main import db

            db.add_user(
                tg_user_id=message.from_user.id,  # type: ignore
                access_token=access_token,
            )


async def _get_hash(message_text: str) -> str | None:
    try:
        hash = message_text.split(" ")[1]
    except IndexError:
        hash = None
    return hash
