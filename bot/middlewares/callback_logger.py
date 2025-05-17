from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from aiogram_dialog.api.entities import Context


class CallbackLoggerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        try:
            result = await handler(event, data)
            context: Context = data['aiogd_context']
            print(
                f"📌 Callback {context.state}:"
                f" {context.dialog_data=} {context.start_data=}"
            )
            return result
        except Exception as e:
            print(f"❌ Error processing callback {event.data}: {str(e)}")
            raise


# Подключение middleware в диспетчер
