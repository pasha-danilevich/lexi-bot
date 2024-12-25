from typing import Any, cast

from aiogram import types
from aiogram.enums.parse_mode import ParseMode
from aiogram.utils import markdown
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import DOMAIN
from markup import buttons, keyboards
from markup.message import NON_AUTHORIZETE, TO_MANY_WORDS, REPRODUCE_TEXT
from models.training import BaseTraining, TrainingManager
from models.word import Word
from state import Reproduce
from utils import (
    escape_markdown_v2,
    get_headers,
    get_response_data,
    get_response_data_patch,
    get_response_data_post,
)


router = Router()

base_trainin_url = f"http://{DOMAIN}/api/training/"
training_url = f"http://{DOMAIN}/api/training/?type=reproduce"


@router.callback_query(F.data == buttons.reproduce_test_cb_data)
async def reproduce_text_handler(callback: CallbackQuery, state: FSMContext):

    await callback.message.answer(  # type: ignore
        text=REPRODUCE_TEXT,
        reply_markup=keyboards.training_text,
    )


@router.callback_query(F.data == buttons.submit_training_cb_data)
async def reproduce_handler(callback: CallbackQuery, state: FSMContext):

    state_data = await state.get_data()
    access_token = state_data.get("access_token", None)

    message = cast(Message, callback.message)

    await state.set_state(Reproduce.text)

    if not access_token:
        await message.answer(text=NON_AUTHORIZETE)
        await state.set_state(None)
        return

    headers = await get_headers(access_token=access_token)

    if headers:
        json_data, status = await get_response_data(
            headers=headers, url=training_url
        )
        if not json_data:
            await message.answer(text=f"Ошибка: {status}")
            await state.set_state(None)
            return

        base_trainings = BaseTraining.make_obj_list(json_data)

        training_manager = TrainingManager(base_trainings)

        await state.update_data(training_manager=training_manager)

        current_training = training_manager.get_current_training()

        if current_training:
            text = display_info(current_training, training_manager)
        else:
            text = "Тест завершен!"
            await state.set_state(None)  # отмета ожидания ввода

        await message.answer(
            text=text,
            # parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=keyboards.reproduce,
        )


@router.message(Reproduce.text)
@router.callback_query(F.data == buttons.next_cb_data)
async def answer_reproduce_handler(
    message: Message | types.CallbackQuery, state: FSMContext
):
    state_data = await state.get_data()
    access_token = state_data.get("access_token", None)
    training_manager: TrainingManager = state_data.get(
        "training_manager", None
    )

    reply_markup = keyboards.reproduce

    if isinstance(message, types.CallbackQuery):
        callback = message
        message = cast(Message, callback.message)
    else:
        user_text: str = str(message.text)
        previous_training = training_manager.get_previous_training()

        if previous_training:
            is_correct = check_answer(user_text, previous_training)
            status = await send_result(
                result=is_correct,
                previous_training=previous_training,
                access_token=access_token,
            )
            if status != 200:
                await message.answer(text="Ошибка")
                await state.set_state(None)
                return
            else:
                text = (
                    "Правильно\\!"
                    if is_correct
                    else f"Не правильно\\. {markdown.bold(previous_training.word.text)}"
                )
                await message.answer(
                    text=text, parse_mode=ParseMode.MARKDOWN_V2
                )

    current_training = training_manager.get_current_training()

    if current_training:

        text = display_info(current_training, training_manager)
    else:
        text = "Тест завершен!"
        reply_markup = keyboards.training
        await state.set_state(None)  # отмета ожидания ввода

    await message.answer(
        text=f"{text}",
        reply_markup=reply_markup,
    )


def display_info(
    current_training: BaseTraining, training_manager: TrainingManager
) -> str:
    current_round = training_manager.round
    length_training = training_manager.length_training
    word = current_training.word
    training = current_training.training
    return f"""{current_round} / {length_training}

{word.translation} ({word.part_of_speech})
lvl: {training.lvl}"""


def check_answer(user_text: str, previous_training: BaseTraining) -> bool:
    word = previous_training.word
    return word.text == user_text.lower().strip()


async def send_result(
    result: bool, previous_training: BaseTraining, access_token: str
) -> int:
    headers = await get_headers(access_token=access_token)

    if not headers:
        return 401

    data = {
        "pk": previous_training.training.pk,  # id записи в таблице Training
        "is_correct": result,
    }
    _, status = await get_response_data_patch(
        headers=headers, url=base_trainin_url, data=data
    )
    return status
