from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from markup import buttons
from models import Translation


translation_list_cd_data_pk_ = "translation_list_cd_data_pk_"


my_profile = InlineKeyboardMarkup(
    inline_keyboard=[[buttons.found_add_word, buttons.training]]
)

training = InlineKeyboardMarkup(
    inline_keyboard=[
        [buttons.recognize, buttons.reproduce],
        [buttons.profile],
    ]
)

add_word = InlineKeyboardMarkup(inline_keyboard=[[buttons.cancel]])

word_info = InlineKeyboardMarkup(
    inline_keyboard=[
        [buttons.add_word, buttons.found_another_word],
        [buttons.profile],
    ]
)

word_added = InlineKeyboardMarkup(
    inline_keyboard=[[buttons.profile, buttons.found_another_word]]
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
            callback_data=f"{translation_list_cd_data_pk_}{translation.pk}",
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
