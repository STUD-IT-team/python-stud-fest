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
from aiogram.utils.keyboard import InlineKeyboardBuilder
from consts import start_msg, reg_complete, text1, text2, text3, text4, text5, text6, text7, text3_2
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile, LinkPreviewOptions
import psycopg2
import os
import qrcode

def get_all_chat_ids():
    conn = psycopg2.connect(
        dbname="bauman_festival_bot",
        user="admin",
        password="admin",
        host="pgrrs",
        port="5432"
    )
    
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT chat_id FROM member;"
        )
        rows = cursor.fetchall()
        chat_ids = [row[0] for row in rows]
        return chat_ids
    except Exception as e:
        print(f"Error getting all TGs: {e}")

    finally:
        cursor.close()
        conn.close()

def add_member_to_db(tg):
    conn = psycopg2.connect(
        dbname="bauman_festival_bot",
        user="admin",
        password="admin",
        host="pgrrs",
        port="5432"
    )

    cursor = conn.cursor()

    try:
        if tg == "":
            defs = get_members_with_default_tg()
            maxn = 0
            for member in defs:
                maxn = max(maxn, int(member['tg'].lstrip('default')))
            cursor.execute(
                "INSERT INTO member (tg) VALUES (%s);",
                (f'default{maxn+1}',)
            )
            conn.commit()
        else:
            cursor.execute(
                "INSERT INTO member (tg) VALUES (%s);",
                (tg,)
            )
            conn.commit()
    except Exception as e:
        print(f"Error adding member: {e}")
    
    finally:
        cursor.close()
        conn.close()

def fill_member_to_db(chat_id, tg, name, group_name):
    conn = psycopg2.connect(
        dbname="bauman_festival_bot",
        user="admin",
        password="admin",
        host="pgrrs",
        port="5432"
    )

    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE member SET chat_id = %s, name = %s, group_name = %s WHERE tg = %s;",
            (chat_id, name, group_name, tg)
        )
        conn.commit()
    except Exception as e:
        print(f"Error adding member: {e}")
    
    finally:
        cursor.close()
        conn.close()

def update_member_chat_id(tg, chat_id):
    conn = psycopg2.connect(
        dbname="bauman_festival_bot",
        user="admin",
        password="admin",
        host="pgrrs",
        port="5432"
    )

    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE member SET chat_id = %s WHERE tg = %s;",
            (chat_id, tg)
        )
        conn.commit()
    except Exception as e:
        print(f"Error updating member: {e}")
    
    finally:
        cursor.close()
        conn.close()

def is_in_db(tg):
    conn = psycopg2.connect(
        dbname="bauman_festival_bot",
        user="admin",
        password="admin",
        host="pgrrs",
        port="5432"
    )
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM member WHERE tg = %s", (tg,))
    
    member = cursor.fetchone()
    
    cursor.close()
    conn.close()
    if member:
        return True
    else:
        return False

def to_fill(tg):
    conn = psycopg2.connect(
        dbname="bauman_festival_bot",
        user="admin",
        password="admin",
        host="pgrrs",
        port="5432"
    )
    cursor = conn.cursor()
    
    cursor.execute("SELECT group_name FROM member WHERE tg = %s", (tg,))
    
    member = cursor.fetchone()

    cursor.close()
    conn.close()
    if member[0] == "Орехи":
        return True
    else:
        return False

def get_in_db(tg):
    conn = psycopg2.connect(
        dbname="bauman_festival_bot",
        user="admin",
        password="admin",
        host="pgrrs",
        port="5432"
    )
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM member WHERE tg = %s", (tg,))
        
        member = cursor.fetchone()
    except Exception as e:
        print(f"Error adding member: {e}")
    
    finally:
        cursor.close()
        conn.close()
        return member

def get_members_with_default_tg():
    conn = psycopg2.connect(
        dbname="bauman_festival_bot",
        user="admin",
        password="admin",
        host="pgrrs",
        port="5432"
    )
    cursor = conn.cursor()
    
    try:
        query = "SELECT tg, name, group_name FROM member WHERE tg LIKE 'default%';"
        cursor.execute(query)
        
        members = cursor.fetchall()
    except Exception as e:
        print(f"Error adding member: {e}")
    
    finally:
        cursor.close()
        conn.close()
        return members

async def send_message_to_users(ids, message_text):
    for chat_id in ids:
        if chat_id == None:
            continue
        try:
            await bot.send_message(chat_id=chat_id, text=message_text)
            print(f"Message sent to {chat_id}")
        except Exception as e:
            print(f"Failed to send message to {username}: {e}")

# Bot token can be obtained via https://t.me/BotFather
TOKEN = "7357167773:AAFRhw7Zr4FMBATfUaHNd96QmXxFrNOuIzI"
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

buttons = ["ИНФО", "Регистрация"]
confirm = ["Верно", "Нет"]
qr = ["ИНФО", "QR"]
admin = ["Плотный @all"]
admin_msg = ["Базара не будет"]

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

def make_kb_admin():
    kb = [
        [
            types.KeyboardButton(text=b) for b in admin
        ],
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Здесь был IT"
    )

    return keyboard

def make_kb_admin_msg():
    kb = [
        [
            types.KeyboardButton(text=b) for b in admin_msg
        ],
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Здесь был IT"
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


class UserStates(StatesGroup):
    Start = State()
    Name = State()
    Group = State()
    Confirm = State()
    QR = State()


class AdminStates(StatesGroup):
    Start = State()
    Msg = State()


Admins = [370394115, 392875761]

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()
router = Router()
dp.include_router(router)

@dp.callback_query(F.data == "1")
async def send_random_value(callback: types.CallbackQuery):
    await callback.answer("ok")
    await callback.bot.delete_message(callback.message.chat.id, callback.message.message_id)
    kb = make_inline_kb_for_kb1()
    await callback.bot.send_message(callback.message.chat.id, f"{text1}",
     reply_markup=kb,
     link_preview_options=LinkPreviewOptions(is_disabled=True))

@dp.callback_query(F.data == "2")
async def send_random_value(callback: types.CallbackQuery):
    await callback.answer("ok")
    await callback.bot.delete_message(callback.message.chat.id, callback.message.message_id)
    kb = make_inline_kb_for_kb2()
    # await callback.bot.send_message(callback.message.chat.id, f"{text2}")
    image_from_pc = FSInputFile(f"plan.png")
    result = await callback.bot.send_photo(
        callback.message.chat.id,
        photo=image_from_pc,
        caption=f"{text2}",
        reply_markup=kb
    )

@dp.callback_query(F.data == "3")
async def send_random_value(callback: types.CallbackQuery):
    await callback.answer("ok")
    await callback.message.answer(f"{text3}",
     link_preview_options=LinkPreviewOptions(is_disabled=True))
    # await callback.bot.delete_message(callback.message.chat.id, callback.message.message_id)
    kb = make_inline_kb_for_kb3()
    await callback.bot.send_message(callback.message.chat.id, f"{text3_2}", reply_markup=kb,
     link_preview_options=LinkPreviewOptions(is_disabled=True))

@dp.callback_query(F.data == "4")
async def send_random_value(callback: types.CallbackQuery):
    await callback.answer("ok")
    await callback.bot.delete_message(callback.message.chat.id, callback.message.message_id)
    kb = make_inline_kb_for_kb4()
    await callback.bot.send_message(callback.message.chat.id, f"{text4}", reply_markup=kb,
     link_preview_options=LinkPreviewOptions(is_disabled=True))

@dp.callback_query(F.data == "5")
async def send_random_value(callback: types.CallbackQuery):
    await callback.answer("ok")
    await callback.bot.delete_message(callback.message.chat.id, callback.message.message_id)
    kb = make_inline_kb_for_kb5()
    await callback.bot.send_message(callback.message.chat.id, f"{text5}", reply_markup=kb,
     link_preview_options=LinkPreviewOptions(is_disabled=True))

@dp.callback_query(F.data == "6")
async def send_random_value(callback: types.CallbackQuery):
    await callback.answer("ok")
    await callback.bot.delete_message(callback.message.chat.id, callback.message.message_id)
    kb = make_inline_kb_for_kb6()
    await callback.bot.send_message(callback.message.chat.id, f"{text6}", reply_markup=kb,
     link_preview_options=LinkPreviewOptions(is_disabled=True))

@dp.callback_query(F.data == "7")
async def send_random_value(callback: types.CallbackQuery):
    await callback.answer("ok")
    await callback.bot.delete_message(callback.message.chat.id, callback.message.message_id)
    kb = make_inline_kb_for_kb7()
    await callback.bot.send_message(callback.message.chat.id, f"{text7}", reply_markup=kb,
     link_preview_options=LinkPreviewOptions(is_disabled=True))

@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext):
    args = message.text
    """
    This handler receives messages with `/start` command
    """
    if message.chat.id in Admins:
        if args and len(args.split('=')) == 2 and args.split('=')[0] == '/start username':
            if args.split('=')[1] == "":
                await message.answer(f"Ник тг недоступен(\nВ базе без ника: {get_members_with_default_tg()}")
            memb = get_in_db(args.split('=')[1])
            if memb:
                await message.answer(f"{memb} зарегистрирован!")
            else:
                await message.answer("Не зарегистрирован")
        else:
            await message.answer(
                text=f"Hello admin, выбери что делать будем?",
                reply_markup=make_kb_admin())
            await state.set_state(AdminStates.Start)
    else:
        if not is_in_db(message.from_user.username):
            add_member_to_db(message.from_user.username)
        if to_fill(message.from_user.username):
            kb = make_kb_start()
            await message.answer(f"Добро пожаловать в бота СтудФеста!", reply_markup=kb)
            await state.set_state(UserStates.Start)
            kkb = make_inline_kb_start()
            await message.answer(text=start_msg, reply_markup=kkb,
                link_preview_options=LinkPreviewOptions(is_disabled=True))
        else:
            update_member_chat_id(message.from_user.username, message.chat.id)
            await message.answer(
                text="Добро пожаловать",
                reply_markup=make_kb_qr()
            )
            await state.set_state(UserStates.QR)

@router.message(AdminStates.Start, F.text.in_(admin))
async def user_fest_admin_start(message: Message, state: FSMContext):
    if message.text == admin[0]:
        await message.answer(
            text="Чего базаришь?", reply_markup=make_kb_admin_msg()
        )
        await state.set_state(AdminStates.Msg)

@router.message(AdminStates.Msg)
async def user_fest_admin_msg(message: Message, state: FSMContext):
    if message.text == admin_msg[0]:
        await message.answer(
            text="Базара нет", reply_markup=make_kb_admin()
        )
        await state.set_state(AdminStates.Start)
    else:
        await send_message_to_users(get_all_chat_ids(), message.text)
        await message.answer(
            text="Базар оформлен", reply_markup=make_kb_admin()
        )
        await state.set_state(AdminStates.Start)


@router.message(UserStates.Start, F.text.in_(buttons))
async def user_fest_rega_start(message: Message, state: FSMContext):
    if message.text == buttons[0]:
        kb = make_inline_kb_start()
        await message.answer(
            text=start_msg, reply_markup=kb
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
        fill_member_to_db(message.chat.id, message.from_user.username, user_data['name'], user_data['group'])
        await message.answer(
            text=reg_complete,
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
        kkb = make_inline_kb_start()
        await message.answer(text=start_msg, reply_markup=kkb)
    elif message.text == qr[1]:
        img = qrcode.make(f'https://t.me/BMSTU_StudFestbot?start=username={message.from_user.username}')
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
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
