# src/state.py

from aiogram.fsm.state import State, StatesGroup


# Определяем состояния
class Token(StatesGroup):
    access_token = State()


class AddWord(StatesGroup):
    text = State()
