from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router()

@router.message(Command("view_token"))
async def view_token_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    token = data.get('access_token')

    if token:
        await message.answer(f"Ваш токен: {token}")
    else:
        await message.answer("Токена нет.")
