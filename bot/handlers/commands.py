from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager

from bot.dialogs.add_word.state import AddWordSG
from bot.dialogs.home.state import HomeSG

router = Router()


@router.message(Command("start"))
@router.message(Command("home"))
async def start_handler(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(HomeSG.home)


@router.message(Command("add"))
async def start_handler(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(AddWordSG.add_word)
