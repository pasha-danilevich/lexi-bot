from aiogram.fsm.state import State, StatesGroup


class AddWordSG(StatesGroup):
    add_word = State()
    search_word = State()
    word_card = State()
    select_collection = State()
    create_associations = State()
    end_add_word = State()
    # branch
    user_word_card = State()
    change_associations = State()
    delete_word = State()
