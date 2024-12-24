from aiogram.types import InlineKeyboardButton

delete_cb_data = "delete_cb_data"
profile_cd_data = "profile_cd_data"
add_word_cb_data = "add_word_cb_data"
select_word_to_add_cd_data = "select_word_to_add_cd_data"

training_cb_data = "training_cb_data"
recognize_test_cb_data = "recognize_test_cb_data"
reproduce_test_cb_data = "reproduce_test_cb_data"

cancel = InlineKeyboardButton(
    text="Отмена",
    callback_data=delete_cb_data,
)

profile = InlineKeyboardButton(
    text="Профиль",
    callback_data=profile_cd_data,
)

found_another_word = InlineKeyboardButton(
    text="Найти другое слово", callback_data=add_word_cb_data
)

found_add_word = InlineKeyboardButton(
    text="Найти / Добавить слово", callback_data=add_word_cb_data
)

add_word = InlineKeyboardButton(
    text="Добавить слово",
    callback_data=select_word_to_add_cd_data,
)

training = InlineKeyboardButton(
    text="Тренировка слов", callback_data=training_cb_data
)

recognize = InlineKeyboardButton(
    text="Тест с выбором ответа",
    callback_data=reproduce_test_cb_data,
)

reproduce = InlineKeyboardButton(
    text="Тест на узнаваемость",
    callback_data=recognize_test_cb_data,
)