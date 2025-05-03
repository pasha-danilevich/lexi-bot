from aiogram.fsm.state import State, StatesGroup


class CollectionSG(StatesGroup):
    collections = State()
