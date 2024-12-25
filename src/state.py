# src/state.py

from aiogram.fsm.state import State, StatesGroup


# Определяем состояния
class Token(StatesGroup):
    access_token = State()


class AddWord(StatesGroup):
    text = State()


class WordInstanse(StatesGroup):
    word_instance = State()


class TrainingManager(StatesGroup):
    training_manager = State()


class Reproduce(StatesGroup):
    text = State()
