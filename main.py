import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html, types
from aiogram import Router, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder


from consts import start_msg, text1, text2, text3, text4, text5, text6, text7, text3_2

# Bot token can be obtained via https://t.me/BotFather
TOKEN = "7357167773:AAFRhw7Zr4FMBATfUaHNd96QmXxFrNOuIzI"


def make_kb_start():
    kb = [
        [
            types.KeyboardButton(text="ИНФО"),
            types.KeyboardButton(text="регистрация")
        ],
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите способ подачи"
    )

    return keyboard

def make_inline_kb_start():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Программа", callback_data="1"
    )
    builder.button(
        text="Расписание", callback_data="2"
    )
    builder.button(
        text="Студенческие Организации", callback_data="3"
    )
    builder.button(
        text="Студенческий Совет", callback_data="4"
    )
    builder.button(
        text="Научные центры", callback_data="5"
    )
    builder.button(
        text="Экскурсии в компании", callback_data="6"
    )
    builder.button(
        text="Наука и искусство", callback_data="7"
    )
    # Выравниваем кнопки по 1 в ряд, чтобы получилось 4 + 1
    builder.adjust(1)
    return builder.as_markup()

def make_inline_kb_for_kb1():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Расписание", callback_data="2"
    )
    builder.button(
        text="Студенческие Организации", callback_data="3"
    )
    builder.button(
        text="Студенческий Совет", callback_data="4"
    )
    builder.button(
        text="Научные центры", callback_data="5"
    )
    builder.button(
        text="Экскурсии в компании", callback_data="6"
    )
    builder.button(
        text="Наука и искусство", callback_data="7"
    )
    # Выравниваем кнопки по 1 в ряд, чтобы получилось 4 + 1
    builder.adjust(1)
    return builder.as_markup()

def make_inline_kb_for_kb2():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Программа", callback_data="1"
    )
    builder.button(
        text="Студенческие Организации", callback_data="3"
    )
    builder.button(
        text="Студенческий Совет", callback_data="4"
    )
    builder.button(
        text="Научные центры", callback_data="5"
    )
    builder.button(
        text="Экскурсии в компании", callback_data="6"
    )
    builder.button(
        text="Наука и искусство", callback_data="7"
    )
    # Выравниваем кнопки по 1 в ряд, чтобы получилось 4 + 1
    builder.adjust(1)
    return builder.as_markup()

def make_inline_kb_for_kb3():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Программа", callback_data="1"
    )
    builder.button(
        text="Расписание", callback_data="2"
    )
    builder.button(
        text="Студенческий Совет", callback_data="4"
    )
    builder.button(
        text="Научные центры", callback_data="5"
    )
    builder.button(
        text="Экскурсии в компании", callback_data="6"
    )
    builder.button(
        text="Наука и искусство", callback_data="7"
    )
    # Выравниваем кнопки по 1 в ряд, чтобы получилось 4 + 1
    builder.adjust(1)
    return builder.as_markup()

def make_inline_kb_for_kb4():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Программа", callback_data="1"
    )
    builder.button(
        text="Расписание", callback_data="2"
    )
    builder.button(
        text="Студенческие Организации", callback_data="3"
    )
    builder.button(
        text="Научные центры", callback_data="5"
    )
    builder.button(
        text="Экскурсии в компании", callback_data="6"
    )
    builder.button(
        text="Наука и искусство", callback_data="7"
    )
    # Выравниваем кнопки по 1 в ряд, чтобы получилось 4 + 1
    builder.adjust(1)
    return builder.as_markup()

def make_inline_kb_for_kb5():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Программа", callback_data="1"
    )
    builder.button(
        text="Расписание", callback_data="2"
    )
    builder.button(
        text="Студенческие Организации", callback_data="3"
    )
    builder.button(
        text="Студенческий Совет", callback_data="4"
    )
    builder.button(
        text="Экскурсии в компании", callback_data="6"
    )
    builder.button(
        text="Наука и искусство", callback_data="7"
    )
    # Выравниваем кнопки по 1 в ряд, чтобы получилось 4 + 1
    builder.adjust(1)
    return builder.as_markup()

def make_inline_kb_for_kb6():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Программа", callback_data="1"
    )
    builder.button(
        text="Расписание", callback_data="2"
    )
    builder.button(
        text="Студенческие Организации", callback_data="3"
    )
    builder.button(
        text="Студенческий Совет", callback_data="4"
    )
    builder.button(
        text="Научные центры", callback_data="5"
    )
    builder.button(
        text="Наука и искусство", callback_data="7"
    )
    # Выравниваем кнопки по 1 в ряд, чтобы получилось 4 + 1
    builder.adjust(1)
    return builder.as_markup()

def make_inline_kb_for_kb7():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Программа", callback_data="1"
    )
    builder.button(
        text="Расписание", callback_data="2"
    )
    builder.button(
        text="Студенческие Организации", callback_data="3"
    )
    builder.button(
        text="Студенческий Совет", callback_data="4"
    )
    builder.button(
        text="Научные центры", callback_data="5"
    )
    builder.button(
        text="Экскурсии в компании", callback_data="6"
    )
    # Выравниваем кнопки по 1 в ряд, чтобы получилось 4 + 1
    builder.adjust(1)
    return builder.as_markup()


class UserFestRega(StatesGroup):
    Name = State()
    Group = State()
    QR = State()


class AdminStates(StatesGroup):
    Start = State()
    Confirm = State()


Admins = []

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()
router = Router()
dp.include_router(router)

@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    """
    This handler receives messages with `/start` command
    """
    if message.chat.id in Admins:
        await message.answer(f"Hello admin, выбери что делать будем? {html.bold(message.from_user.full_name)}!")
        await state.set_state(AdminStates.Start)
    else:
        await state.set_state(UserFestRega.Name)
        kb = make_kb_start()

        await message.answer(f"Hello user, {html.bold(message.from_user.full_name)}! введи ФИО", reply_markup=kb)

        kkb = make_inline_kb_start()

        await message.answer(start_msg, reply_markup=kkb)


@dp.callback_query(F.data == "1")
async def send_random_value(callback: types.CallbackQuery):
    await callback.answer("ok")
    await callback.bot.delete_message(callback.message.chat.id, callback.message.message_id)
    kb = make_inline_kb_for_kb1()
    await callback.bot.send_message(callback.message.chat.id, f"текст {text1}", reply_markup=kb)

@dp.callback_query(F.data == "2")
async def send_random_value(callback: types.CallbackQuery):
    await callback.answer("ok")
    await callback.bot.delete_message(callback.message.chat.id, callback.message.message_id)
    kb = make_inline_kb_for_kb2()
    await callback.bot.send_message(callback.message.chat.id, f"текст {text2}", reply_markup=kb)

@dp.callback_query(F.data == "3")
async def send_random_value(callback: types.CallbackQuery):
    await callback.answer("ok")
    await callback.message.answer(f"текст {text3}")
    await callback.bot.delete_message(callback.message.chat.id, callback.message.message_id)
    kb = make_inline_kb_for_kb3()
    await callback.bot.send_message(callback.message.chat.id, f"текст {text3_2}", reply_markup=kb)

@dp.callback_query(F.data == "4")
async def send_random_value(callback: types.CallbackQuery):
    await callback.answer("ok")
    await callback.bot.delete_message(callback.message.chat.id, callback.message.message_id)
    kb = make_inline_kb_for_kb4()
    await callback.bot.send_message(callback.message.chat.id, f"текст {text4}", reply_markup=kb)

@dp.callback_query(F.data == "5")
async def send_random_value(callback: types.CallbackQuery):
    await callback.answer("ok")
    await callback.bot.delete_message(callback.message.chat.id, callback.message.message_id)
    kb = make_inline_kb_for_kb5()
    await callback.bot.send_message(callback.message.chat.id, f"текст {text5}", reply_markup=kb)

@dp.callback_query(F.data == "6")
async def send_random_value(callback: types.CallbackQuery):
    await callback.answer("ok")
    await callback.bot.delete_message(callback.message.chat.id, callback.message.message_id)
    kb = make_inline_kb_for_kb6()
    await callback.bot.send_message(callback.message.chat.id, f"текст {text6}", reply_markup=kb)

@dp.callback_query(F.data == "7")
async def send_random_value(callback: types.CallbackQuery):
    await callback.answer("ok")
    await callback.bot.delete_message(callback.message.chat.id, callback.message.message_id)
    kb = make_inline_kb_for_kb7()
    await callback.bot.send_message(callback.message.chat.id, f"текст {text7}", reply_markup=kb)


@router.message(UserFestRega.Name)
async def user_fest_rega_name(message: Message, state: FSMContext):
    await message.answer(
        text="введите вашу группу:",
    )
    await state.set_state(UserFestRega.Group)


@router.message(UserFestRega.Group)
async def food_chosen_incorrectly(message: Message, state: FSMContext):
    await message.answer(
        text="получаем qr",
    )
    await state.set_state(UserFestRega.QR)


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    print(TOKEN)
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())


