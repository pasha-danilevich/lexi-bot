import pprint
from typing import Any, Awaitable, Callable, Dict
from aiogram.fsm.context import FSMContext
from aiogram import BaseMiddleware
from aiogram.types import Message

from markup.message import NON_AUTHORIZETE
from models.user import User


class CounterMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:

        state: FSMContext = data["state"]
        message: Message = data["event_update"].message

        state_data = await state.get_data()
        access_token = state_data.get("access_token", None)

        if not access_token:

            user = User(message=message)

            if user.is_correct_access_token():
                accest_token_from_user = user.get_access_token()
                access_token = await state.update_data(
                    access_token=accest_token_from_user
                )
            else:
                access_token = await state.update_data(access_token=None)

        return await handler(event, data)
