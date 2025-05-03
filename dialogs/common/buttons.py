from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const

from dialogs.home.state import HomeSG

HOME = Start(Const('На главную'), state=HomeSG.home, id='home')
