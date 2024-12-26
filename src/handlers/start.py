# src/handler.py

import aiohttp
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from markup import message as text_message
from config import DOMAIN
from models.user import User
from utils import check_access_token, print_with_location


router = Router()
url = f"http://{DOMAIN}/api/tg-auth/"


@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):

    access_token = await check_context_state_access_token(
        message=message, state=state
    )
    if access_token:
        print_with_location('state auth')
        return # завершаем

    await message.answer(text=text_message.START_MESSEGE)

    if message.text:
        hash_code = await _get_hash(message_text=message.text)

        from main import db

        user_id = message.from_user.id  # type: ignore

        if hash_code:

            access_token = await get_access_token_from_hash(
                hash_code=hash_code, message=message
            )
            
            if access_token == 'error':
                return # завершаем

            if access_token:

                await state.update_data(access_token=access_token)

                has_update = db.edit_access_token(
                    tg_user_id=user_id, new_access_token=access_token
                )
                if not has_update:
                    db.add_user(
                        tg_user_id=message.from_user.id,  # type: ignore
                        access_token=access_token,
                    )

                await message.answer(text=text_message.YOU_AUTH_MESSEGE)
            else:
                await message.answer(text=text_message.ERROR_GET_ACCESS_TOKEN)

        else:  # start без hash

            user_tuple = db.get_user(tg_user_id=user_id)
            user = None

            if user_tuple:
                user = User(message=message, user=user_tuple)

            if not user:
                await message.answer(text=text_message.YOU_ARE_FIRST)
                db.add_user(
                    tg_user_id=message.from_user.id,  # type: ignore
                    access_token=None,
                )
            else:
                # актуален ли access_token у user

                if user.is_correct_access_token():
                    await state.update_data(access_token=user.access_token)
                    await message.answer(text=text_message.YOU_AUTH_MESSEGE)
                else:
                    await message.answer(text=text_message.TOKEN_HAS_EXPIRED)


async def _get_hash(message_text: str) -> str | None:
    try:
        hash = message_text.split(" ")[1]
    except IndexError:
        hash = None
    return hash


async def check_context_state_access_token(
    message: Message, state: FSMContext
) -> str | None:
    state_data = await state.get_data()
    access_token = state_data.get("access_token", None)

    if access_token:
        if check_access_token(access_token):
            await message.answer(text=text_message.ALREADY_AUTHORIZED)
            return access_token
        else:
            await message.answer(text=text_message.TOKEN_HAS_EXPIRED)
            return None


async def get_access_token_from_hash(
    hash_code: str, message: Message
) -> str:
    url_params = url + f"?hash={hash_code}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url_params) as response:
            if response.status == 200:
                access_token = await response.json()
                return access_token

            elif response.status == 404:
                await message.answer(text=text_message.ERROR_GET_ACCESS_TOKEN)
                return 'error'
            else:
                await message.answer(
                    text=text_message.UNEXPECTED_ERROR_GET_ACCESS_TOKEN
                )
                return 'error'
