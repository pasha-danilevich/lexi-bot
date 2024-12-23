from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from models import Translation


random_num_updated_cb_data = "random_num_updated_cb_data"
add_word_cb_data = "add_word_cb_data"
training_cb_data = "training_cb_data"
profile_cd_data = "profile_cd_data"
add_word_to_dict_cd_data = "add_word_to_dict_cd_data"

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
        ],
        [
            InlineKeyboardButton(
                text="Профиль",
                callback_data=profile_cd_data,
            ),
        ],
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
                text="Найти другое слово", callback_data=add_word_cb_data
            ),
        ],
        [InlineKeyboardButton(text="Профиль", callback_data=profile_cd_data)],
    ]
)


def get_translation_list(
    translations: list[Translation], related_pk: list[int]
) -> InlineKeyboardMarkup:
    buttons = []
    buttons_line = []
    
    local_related_pk = related_pk.copy()

    for translation in translations:
        # Если перевод слова есть у пользователя, то пропускаем его
        if translation.pk in local_related_pk:
            local_related_pk.remove(translation.pk)
            continue  

        button = InlineKeyboardButton(
            text=translation.text,
            callback_data=f"translation_list_cd_data_pk_{translation.pk}",
        )
        buttons_line.append(button)

        # Если достигли лимита в 3 кнопки, добавляем текущую строку в buttons
        if len(buttons_line) == 3:
            buttons.append(buttons_line)
            buttons_line = []  # Начинаем новую строку

    # Добавляем оставшиеся кнопки, если они есть
    if buttons_line:
        buttons.append(buttons_line)

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def build_actions_kb(
    button_text="Random number",
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=button_text,
        callback_data=random_num_updated_cb_data,
    )
    return builder.as_markup()
