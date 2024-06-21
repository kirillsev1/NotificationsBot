from aiogram import types
from aiogram.filters.command import Command

from src.hendlers.notes.router import main_router


@main_router.message(
    Command(
        'start',
    )
)
async def cmd_start(message: types.Message) -> None:
    await message.answer('Спасибо что пришли')
