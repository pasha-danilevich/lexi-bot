from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Создание клавиатуры с кнопками
main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Каталог")],
        [KeyboardButton(text="Корзина"), KeyboardButton(text="Контакты")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню.",
)

# Создание инлайн-клавиатуры
settings = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="YouTube", url="https://youtube.com/@sudoteach"
            )
        ]
    ]
)

# Список автомобилей
cars = ["Tesla", "Mercedes", "BMW", "Porsche"]


async def inline_cars():
    keyboard = InlineKeyboardBuilder()
    for car in cars:
        keyboard.add(
            InlineKeyboardButton(text=car, callback_data=f"car_{car}")
        )
    return keyboard.adjust(2).as_markup()
