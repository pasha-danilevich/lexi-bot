import time
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
from markup.message import (
    NON_AUTHORIZETE,
    RECOGNIZE_TEXT,
    TO_MANY_WORDS,
    REPRODUCE_TEXT,
)
from models.training import BaseTraining, TrainingManager
from models.word import Word
from state import Reproduce
from utils import (
    escape_markdown_v2,
    get_headers,
    get_response_data,
    get_response_data_patch,
    get_response_data_post,
    print_with_location,
)


router = Router()

base_trainin_url = f"http://{DOMAIN}/api/training/"
training_url = f"http://{DOMAIN}/api/training/?type=recognize"


@router.callback_query(F.data == buttons.recognize_test_cb_data)
async def recognize_text_handler(callback: CallbackQuery, state: FSMContext):

    await callback.message.answer(  # type: ignore
        text=RECOGNIZE_TEXT,
        reply_markup=keyboards.training_text_recognize,
    )


@router.callback_query(F.data == buttons.submit_recognize_cb_data)
async def recognize_handler(callback: CallbackQuery, state: FSMContext):

    state_data = await state.get_data()
    access_token = state_data.get("access_token", None)

    message = cast(Message, callback.message)
    # TODO
    # имя state класса под вопросом
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

        if current_training and current_training.false_set:
            text = display_info(current_training, training_manager)
            await message.answer(
                text=text,
                reply_markup=keyboards.get_false_set_keyboard(
                    false_set=current_training.false_set
                ),
            )
        else:
            text = "Тест завершен!"
            await message.answer(
                text=text,
            )
            await state.set_state(None)  # отмета ожидания ввода


@router.callback_query(F.data.startswith(keyboards.false_set_cd_data_index_))
@router.callback_query(F.data == buttons.next_recognize_cb_data)
async def answer_reproduce_handler(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    access_token = state_data.get("access_token", None)
    training_manager: TrainingManager = state_data.get(
        "training_manager", None
    )

    message = cast(Message, callback.message)

    if callback.data:
        if callback.data == buttons.next_recognize_cb_data:
            # просто отображаем след. слово
            await show_word(
                training_manager=training_manager, state=state, message=message
            )
        elif F.data.startswith(keyboards.false_set_cd_data_index_):
            # делаем проверку и отобаржаем след. слово
            id_selected_word: int = int(callback.data.split("_")[-1])
            previous_training = training_manager.get_previous_training()

            if previous_training:
                await check_answer_show_result_message(
                    id_selected_word=id_selected_word,
                    previous_training=previous_training,
                    access_token=access_token,
                    message=message,
                    state=state,
                )
            time.sleep(1)
            await show_word(
                training_manager=training_manager, state=state, message=message
            )
        else:
            await message.edit_text(text=f"Неизвестная команда")


async def show_word(
    training_manager: TrainingManager, state: FSMContext, message: Message
):
    current_training = training_manager.get_current_training()

    if current_training and current_training.false_set:
        reply_markup = keyboards.get_false_set_keyboard(
            false_set=current_training.false_set
        )
        text = display_info(current_training, training_manager)
    else:
        text = "Тест завершен!"
        reply_markup = keyboards.training
        await state.set_state(None)  # отмета ожидания ввода

    await message.edit_text(
        text=f"{text}",
        reply_markup=reply_markup,
    )


async def check_answer_show_result_message(
    id_selected_word: int,
    previous_training: BaseTraining,
    access_token: str,
    message: Message,
    state: FSMContext,
):
    is_correct = check_answer(id_selected_word, previous_training)
    status = await send_result(
        result=is_correct,
        previous_training=previous_training,
        access_token=access_token,
    )
    if status != 200:
        await message.answer(
            text="Ошибка, проверка этого слова не прошла. Повторите позже."
        )
        await state.set_state(None)
        return

    keyboard = None
    if previous_training.false_set:
        keyboard = keyboards.get_false_set_after_answer_keyboard(
            is_correct=is_correct,
            false_set=previous_training.false_set,
            id_selected_word=id_selected_word,
        )
    await message.edit_reply_markup(reply_markup=keyboard)


def display_info(
    current_training: BaseTraining, training_manager: TrainingManager
) -> str:
    current_round = training_manager.round
    length_training = training_manager.length_training
    word = current_training.word
    training = current_training.training
    return f"""Раунд:                                              {current_round} / {length_training}

{word.text} 
[ {word.transcription} ] {word.part_of_speech}.
lvl: {training.lvl}"""


def check_answer(
    id_selected_word: int, previous_training: BaseTraining
) -> bool:
    selected_word = None

    if previous_training.false_set:
        selected_word = previous_training.false_set.words[id_selected_word]
    word = previous_training.word
    return word.translation == selected_word


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
