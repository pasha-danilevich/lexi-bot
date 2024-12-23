from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


random_num_updated_cb_data = "random_num_updated_cb_data"
add_word_cb_data = "add_word_cb_data"
training_cb_data = "training_cb_data"
profile_cd_data = "profile_cd_data"
add_word_to_dict_cd_data = "add_word_to_dict_cd_data"
meaning_cb_data = "meaning_cb_data"

recognize_test_cb_data = "recognize_test_cb_data"
reproduce_test_cb_data = "reproduce_test_cb_data"


my_profile = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Найти / Добавить слово", callback_data=add_word_cb_data
            ),
            InlineKeyboardButton(
                text="Тренировка слов", callback_data=training_cb_data
            ),
        ]
    ]
)

training = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Тест на узнаваемость",
                callback_data=recognize_test_cb_data,
            ),
            InlineKeyboardButton(
                text="Тест с выбором ответа",
                callback_data=reproduce_test_cb_data,
            ),
            InlineKeyboardButton(
                text="Профиль", callback_data=profile_cd_data
            ),
        ]
    ]
)

add_word = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Вернуться в профиль",
                callback_data=profile_cd_data,
            )
        ]
    ]
)

word_info = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Добавить слово",
                callback_data=add_word_to_dict_cd_data,
            ),
            InlineKeyboardButton(
                text="Близкие по значению",
                callback_data=meaning_cb_data,
            ),
            InlineKeyboardButton(
                text="Профиль", callback_data=profile_cd_data
            ),
            InlineKeyboardButton(
                text="Найти другое слово", callback_data=add_word_cb_data
            ),
        ]
    ]
)


def build_actions_kb(
    button_text="Random number",
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=button_text,
        callback_data=random_num_updated_cb_data,
    )
    return builder.as_markup()
