import json

from aiogram import types, F, Router
from aiogram.filters import Command

from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from repository import (get_quiz_index, update_quiz_index, add_quiz_statistic,
                        get_user_quiz_statistic)
from settings.config import QUIZ_DATA

quiz_router = Router()

# Загрузить квиз
try:
    with open(QUIZ_DATA, "r", encoding="utf-8") as f:
        quiz_data = json.load(f)
except (FileNotFoundError, json.decoder.JSONDecodeError):
    quiz_data = []


def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()

    for option in answer_options:
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data="right_answer" if option == right_answer else "wrong_answer")
        )

    builder.adjust(1)
    return builder.as_markup()


async def answer(callback: types.CallbackQuery, text: str = 'Верно!'):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    await callback.message.answer(text)

    current_question_index = await get_quiz_index(callback.from_user.id)
    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)

    result = True if text == 'Верно!' else False
    await add_quiz_statistic(callback.from_user.id, current_question_index, result)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")
        await send_user_result_statistic(callback.message, callback.from_user.id)


@quiz_router.callback_query(F.data == "right_answer")
async def right_answer(callback: types.CallbackQuery):
    await answer(callback, "Верно!")


@quiz_router.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):
    # Получение текущего вопроса из словаря состояний пользователя
    current_question_index = await get_quiz_index(callback.from_user.id)

    correct_option = quiz_data[current_question_index]['correct_option']
    text = (f"Неправильно. Правильный ответ: "
            f"{quiz_data[current_question_index]['options'][correct_option]}")

    await answer(callback, text)


# Хэндлер на команду /start
@quiz_router.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    await message.answer("Добро пожаловать в квиз!",
                         reply_markup=builder.as_markup(resize_keyboard=True))


async def get_question(message, user_id):
    # Получение текущего вопроса из словаря состояний пользователя
    current_question_index = await get_quiz_index(user_id)
    try:
        index = quiz_data[current_question_index]
    except IndexError:
        return await message.answer("технические проблемы")
    correct_index = index['correct_option']
    opts = index['options']
    kb = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(f"{index['question']}",
                         reply_markup=kb)


async def send_user_result_statistic(message, user_id):
    # Вывод статистики ответов пользователя
    user_quiz_statistic = await get_user_quiz_statistic(user_id)

    message_statistic = ''
    for row in user_quiz_statistic:
        answer_result = 'верно' if row[2] else 'неверно'
        message_statistic += (f"номер вопроса: {row[1]} попыток: {row[0]} "
                              f"результат ответа {answer_result}\n")
    await message.answer(message_statistic)


async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0
    await update_quiz_index(user_id, current_question_index)
    await get_question(message, user_id)


# Хэндлер на команду /quiz
@quiz_router.message(F.text == "Начать игру")
@quiz_router.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    await message.answer(f"Давайте начнем квиз!")
    await new_quiz(message)
