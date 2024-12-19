import pprint
from typing import Any, Awaitable, Callable, Dict
from aiogram.fsm.context import FSMContext
from aiogram import BaseMiddleware
from aiogram.types import Message

from message import NON_AUTHORIZETE
from utils import get_user


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

            accest_token_from_db = await get_access_token_from_db(
                message=message, state=state
            )

            access_token = await state.update_data(
                access_token=accest_token_from_db
            )

        return await handler(event, data)


async def get_access_token_from_db(
    message: Message, state: FSMContext
) -> str | None:

    access_token = None
    from main import db

    user = await get_user(message=message, db=db)
    if user:
        access_token = user.access_token

    return access_token
