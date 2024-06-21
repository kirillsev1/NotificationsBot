from aiogram.types import InlineKeyboardButton

from src.callbacks.notes.data.pagination import PaginationCallback


async def get_header(page, date):
    return [
        [
            InlineKeyboardButton(text='hide', callback_data='hide_content'),
            InlineKeyboardButton(text='cancel', callback_data='cancel'),
            InlineKeyboardButton(text='update', callback_data=PaginationCallback(page=page, date=date).pack()),
            InlineKeyboardButton(text='create', callback_data='create_note'),
        ]
    ]
