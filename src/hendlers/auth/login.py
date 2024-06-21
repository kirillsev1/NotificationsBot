from aiogram import types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiohttp import ClientResponseError

from conf.config import settings
from src.hendlers.auth.router import auth_router
from src.utils.request import do_request
from src.state.main import MainState

kb = [
    [
        KeyboardButton(text='Navigation Calendar w month'),
    ],
    [
        KeyboardButton(text='Dialog Calendar w month'),
    ],
]
start_kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


@auth_router.message(Command('login'))
async def cmd_login(message: types.Message, state: FSMContext) -> None:
    await message.answer('enter password')
    await state.set_state(MainState.auth_password)


@auth_router.message(MainState.auth_password)
async def enter_password(message: types.Message, state: FSMContext):
    password = message.text
    if message.from_user is None:
        await message.answer('Something went wrong')
        return
    try:
        data = await do_request(
            f'{settings.BACKEND_HOST}/api/v1/auth/login',
            body={
                'tg_id': message.chat.id,
                'password': password,
            },
        )
    except ClientResponseError:
        await message.answer('Wrong password')
        return

    await state.update_data(data)
    await state.set_state(None)
    await message.answer(
        'Authorization completed',
        reply_markup=start_kb,
    )