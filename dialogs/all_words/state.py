from aiogram.fsm.state import State, StatesGroup


class AllWordSG(StatesGroup):
    all_words = State()
    search_word = State()
    not_found_word = State()
