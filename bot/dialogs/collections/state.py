from aiogram.fsm.state import State, StatesGroup


class CollectionSG(StatesGroup):
    collections = State()
    create_collection = State()
    add_description = State()
