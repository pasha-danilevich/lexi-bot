from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const

from .state import Home

dialog = Dialog(Window(Const("Hello!"), state=Home.home), )