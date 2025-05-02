from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager

from dialogs.home.state import Home

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(Home.home)