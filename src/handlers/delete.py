from typing import cast

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from markup import buttons


router = Router()


@router.callback_query(F.data == buttons.delete_cb_data)
async def delete_handler(callback: CallbackQuery, state: FSMContext):

    message = cast(Message, callback.message)
    await state.set_state(None) # отмета ожидания ввода
    await message.delete()
