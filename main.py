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
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile
import psycopg2
import os
import qrcode

conn = psycopg2.connect(
        dbname="bauman_festival_bot",
        user="admin",
        password="admin",
        host="localhost",
        port="5432"
    )

def add_member_to_db(tg, name, group_name):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO member (tg, name, group_name) VALUES (%s, %s, %s)",
        (tg, name, group_name)
    )
    conn.commit()
    cursor.close()

def is_in_db(tg):
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM member WHERE tg = %s", (tg,))
    
    member = cursor.fetchone()
    
    cursor.close()
    if member:
        return True
    else:
        return False

# Bot token can be obtained via https://t.me/BotFather
# TOKEN = "7357167773:AAFRhw7Zr4FMBATfUaHNd96QmXxFrNOuIzI"
TOKEN="7440370718:AAFulqCFuqugyU0iwLiqX_NC-zOlyM2ixho"

buttons = ["ИНФО", "Регистрация"]
confirm = ["Верно", "Нет"]
qr = ["ИНФО", "QR"]

def make_kb_start():
    kb = [
        [
            types.KeyboardButton(text=b) for b in buttons
        ],
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Здесь был IT"
    )

    return keyboard

def make_kb_confirm():
    kb = [
        [
            types.KeyboardButton(text=b) for b in confirm
        ],
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Здесь был IT"
    )

    return keyboard

def make_kb_qr():
    kb = [
        [
            types.KeyboardButton(text=b) for b in qr
        ],
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Здесь был IT"
    )

    return keyboard

class UserStates(StatesGroup):
    Start = State()
    Name = State()
    Group = State()
    Confirm = State()
    QR = State()


class AdminStates(StatesGroup):
    Start = State()
    Confirm = State()


Admins = [370394115]

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()
router = Router()
dp.include_router(router)

@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext):
    args = message.text
    print(args)
    """
    This handler receives messages with `/start` command
    """
    if message.chat.id in Admins:
        if args:
            params = args.split('=')
            if len(params) == 2 and params[0] == '/start username' and is_in_db(params[1]):
                await message.answer(f"{params[1]} зарегистрирован!")
            else:
                await message.answer("Не зарегистрирован")
        else:
            await message.answer(
                text=f"Hello admin, выбери что делать будем?",
                reply_markup=ReplyKeyboardRemove())
            await state.set_state(AdminStates.Start)
    elif not is_in_db(message.from_user.username):
        kb = make_kb_start()
        await message.answer(f"StartMsg", reply_markup=kb)
        await state.set_state(UserStates.Start)
    else:
        await message.answer(
            text="Добро пожаловать",
            reply_markup=make_kb_qr()
        )
        await state.set_state(UserStates.QR)

@router.message(UserStates.Start, F.text.in_(buttons))
async def user_fest_rega_start(message: Message, state: FSMContext):
    if message.text == buttons[0]:
        await message.answer(
            text="InfMsg"
        )
    elif message.text == buttons[1]:
        await message.answer(
            text="Введите ФИО:",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(UserStates.Name)

@router.message(UserStates.Name)
async def user_fest_rega_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        text="Введите вашу группу:"
    )
    await state.set_state(UserStates.Group)


@router.message(UserStates.Group)
async def user_fest_rega_group(message: Message, state: FSMContext):
    await state.update_data(group=message.text)
    kb = make_kb_confirm()
    user_data = await state.get_data()
    await message.answer(
        text=f"Подтверди данные:\nФИО: {user_data['name']}\nГруппа: {user_data['group']}",
        reply_markup=kb
    )
    await state.set_state(UserStates.Confirm)

@router.message(UserStates.Confirm, F.text.in_(confirm))
async def user_fest_rega_confirm(message: Message, state: FSMContext):
    if message.text == confirm[0]:
        user_data = await state.get_data()
        add_member_to_db(message.from_user.username, user_data['name'], user_data['group'])
        await message.answer(
            text="Спасибо за регистрацию на СтудФест!",
            reply_markup=make_kb_qr()
        )
        await state.set_state(UserStates.QR)
    elif message.text == confirm[1]:
        await message.answer(
            text="Введите ФИО:",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(UserStates.Name)

@router.message(UserStates.QR, F.text.in_(qr))
async def user_fest_rega_qr(message: Message, state: FSMContext):
    if message.text == qr[0]:
        await message.answer(
            text="InfMsg"
        )
    elif message.text == qr[1]:
        img = qrcode.make(f'https://t.me/Stud_fest_Bot?start=username={message.from_user.username}')
        img.save(f"qr_{message.from_user.username}.png")
        image_from_pc = FSInputFile(f"qr_{message.from_user.username}.png")
        result = await message.answer_photo(
            image_from_pc
        )
        os.remove(f"qr_{message.from_user.username}.png")


@router.message()
async def unknown_command(message: types.Message):
    await message.answer(text="Неверная команда. Введите /start для выбора опций.")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    print(TOKEN)
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
