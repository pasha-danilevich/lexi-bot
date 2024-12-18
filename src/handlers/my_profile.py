from typing import Any

import aiohttp
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import DOMAIN
from message import NON_AUTHORIZETE
from utils import get_user


router = Router()

home_url = f"http://{DOMAIN}/api/home/"
training_url = f"http://{DOMAIN}/api/training/info/"


@router.message(Command("my_profile"))
async def view_token_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    access_token = data.get("access_token")

    if not access_token:
        print("not access_token")
        from main import db

        user = await get_user(message=message, db=db)
        if user:
            access_token_data = await state.update_data(
                access_token=user.access_token
            )
            access_token = access_token_data.get("access_token")
        else:
            await message.answer(text=NON_AUTHORIZETE)

    headers = await get_headers(access_token=access_token)

    if headers:
        home_data = await get_response_data(headers, home_url)
        training_data = await get_response_data(headers, training_url)
        await message.answer(f"Ваш токен: {home_data}, {training_data}")
    else:
        await message.answer("Токена нет.")


async def get_response_data(headers, url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                print(f"Ошибка: {response.status}")
                return None


async def get_headers(access_token: str | Any | None) -> dict[str, str] | None:
    if access_token is not None:
        headers = {"Authorization": f"Beare {access_token}"}
        return headers
    else:
        return None
