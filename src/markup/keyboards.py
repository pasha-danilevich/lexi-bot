from unittest import result
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from markup import buttons
from models.training import FalseSet
from models.word import Translation


translation_list_cd_data_pk_ = "translation_list_cd_data_pk_"
false_set_cd_data_index_ = "false_set_cd_data_index_"


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

training_text_recognize = InlineKeyboardMarkup(
    inline_keyboard=[[buttons.cancel, buttons.submit_recognize]]
)
training_text_reproduce = InlineKeyboardMarkup(
    inline_keyboard=[[buttons.cancel, buttons.submit_reproduce]]
)

reproduce = InlineKeyboardMarkup(
    inline_keyboard=[[buttons.cancel, buttons.next_word_reproduce]]
)
reproduce = InlineKeyboardMarkup(
    inline_keyboard=[[buttons.cancel, buttons.next_word_reproduce]]
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


def get_false_set_after_answer_keyboard(
    is_correct: bool, false_set: FalseSet, id_selected_word: int
):
    buttons_list = []

    for index, word in enumerate(false_set.words):
        text = None
        result = "Верно" if is_correct else "Не верно"

        if index == id_selected_word:
            text = f"{word} - {result}"
        else:
            text = word

        button = InlineKeyboardButton(
            text=text,
            callback_data="none",
        )
        buttons_list.append([button])

    buttons_list.append(
        [
            InlineKeyboardButton(
                text="Отмена",
                callback_data="none",
            ),
            InlineKeyboardButton(
                text="Пропустить",
                callback_data="none",
            ),
        ]
    )

    # Формируем клавиатуру
    return InlineKeyboardMarkup(inline_keyboard=buttons_list)


def get_false_set_keyboard(false_set: FalseSet) -> InlineKeyboardMarkup:
    buttons_list = []

    random_words = false_set.get_all_random_false_set()
    # Создание кнопок для каждого слова в false_set
    for index, word in enumerate(random_words):
        button = InlineKeyboardButton(
            text=word,
            callback_data=f"{false_set_cd_data_index_}{index}",
        )
        buttons_list.append([button])

    buttons_list.append([buttons.cancel, buttons.next_word_recognize])

    # Формируем клавиатуру
    return InlineKeyboardMarkup(inline_keyboard=buttons_list)
