import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html, types
from aiogram import Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

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


