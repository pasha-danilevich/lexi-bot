# src/handler.py

from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command


import message as text_message

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    
    from main import db
    
    await message.answer(
        text=text_message.START_MESSEGE
    )
    
    token = None
    
    if message.text:
        token = await get_access_token(message_text=message.text)
        await state.update_data(access_token=token)
        
    if message.from_user:
        user_id = message.from_user.id
        
    if not token:
        user = db.get_user(tg_user_id=user_id)

        if not user:
            await message.answer(
                text=text_message.YOU_ARE_FIRST
            )
        else:
            # актуален ли access_token у user
            ...
    else:
        await message.answer(
            text=text_message.YOU_AUTH_MESSEGE
        )
        user = db.get_user(tg_user_id=user_id)

        if not user:
            db.add_user(tg_user_id=user_id, access_token=token)


async def get_access_token(message_text: str) -> str | None:
    try:
        token = message_text.split(' ')[1] 
    except IndexError:
        token = None      
    return token

        

