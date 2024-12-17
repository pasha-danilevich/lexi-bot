# src/handler.py

import aiohttp
from aiogram import types

from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command

from config import DOMAIN
from database import Database, User
import message as text_message

router = Router()
url = f"http://{DOMAIN}/api/tg-auth/"

@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    
    from main import db
    
    await message.answer(
        text=text_message.START_MESSEGE
    )
    
    token = None
    
    
    if message.text:
        hash_value = await _get_hash(message_text=message.text)  
        
        if hash_value:
            url_params = url + f"?hash={hash_value}"

            async with aiohttp.ClientSession() as session:
                async with session.get(url_params) as response:
                    if response.status == 200:
                        token = await response.json()
                        
                        await state.update_data(access_token=token)  
                    else:
                        await message.answer(
                            text=text_message.ERROR_GET_ACCESS_TOKEN
                        )

    user = await _get_user(message=message, db=db)     

    if not token:
        if not user:
            await message.answer(
                text=text_message.YOU_ARE_FIRST
            )
        else:
            # актуален ли access_token у user

            if user.is_correct_access_token():
                await message.answer(
                    text=text_message.YOU_AUTH_MESSEGE
                )
            else:
                await message.answer(
                    text=text_message.TOKEN_HAS_EXPIRED
                )           
    else:
        await message.answer(
            text=text_message.YOU_AUTH_MESSEGE
        )
        db.edit_access_token(
            tg_user_id=message.from_user.id, # type: ignore
            new_access_token=token
        )
        if not user:
            db.add_user(
                tg_user_id=message.from_user.id, # type: ignore
                access_token=token
             ) 


async def _get_hash(message_text: str) -> str | None:
    try:
        hash = message_text.split(' ')[1] 
    except IndexError:
        hash = None      
    return hash

async def _get_user(message: Message, db: Database) -> User | None:
    if message.from_user:
        user_id = message.from_user.id
        
    user_data = db.get_user(tg_user_id=user_id)

    if user_data:
        user = User(user_data=user_data )
    else:
        user = None
    
    return user



