import pprint
from typing import Any, Awaitable, Callable, Dict
from aiogram.fsm.context import FSMContext
from aiogram import BaseMiddleware
from aiogram.types import Message

from markup.message import NON_AUTHORIZETE
from models.user import User
from utils import print_with_location


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
        print_with_location('state token' if access_token else 'not state token')
        if not access_token:
            from main import db

            user_id = message.from_user.id  # type: ignore

            user_tuple = db.get_user(tg_user_id=user_id)

            if user_tuple:
                user = User(message=message, user=user_tuple)
                if user.is_correct_access_token():
                    accest_token_from_user = user.get_access_token()
                    access_token = await state.update_data(
                        access_token=accest_token_from_user
                    )
                    print_with_location('db token' if access_token else 'not db token')
                else:
                    access_token = await state.update_data(access_token=None)
        
        return await handler(event, data)
