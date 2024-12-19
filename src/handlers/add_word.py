from typing import Any

import aiohttp
from aiogram.enums.parse_mode import ParseMode
from aiogram.utils import markdown
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import DOMAIN
from message import NON_AUTHORIZETE
from utils import get_user


router = Router()


@router.message(Command("add_word"))
async def add_word_handler(message: Message, state: FSMContext):
    state_data = await state.get_data()
    access_token = state_data.get("access_token", None)
    
    if not access_token:
        await message.answer(text=NON_AUTHORIZETE)
        return
    
    await message.answer(text=access_token)